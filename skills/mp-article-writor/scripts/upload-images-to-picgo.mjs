#!/usr/bin/env node

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

function fail(message) {
  console.error(message);
  process.exit(1);
}

function parseArgs(argv) {
  const result = { files: [], dryRun: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--article-title') result.articleTitle = argv[++index];
    else if (arg === '--endpoint') result.endpoint = argv[++index];
    else if (arg === '--file') result.files.push(argv[++index]);
    else if (arg === '--dry-run') result.dryRun = true;
    else fail(`未知参数：${arg}`);
  }
  if (!result.articleTitle) fail('缺少 --article-title');
  if (result.files.length === 0) fail('至少需要一个 --file "角色=/绝对路径"');
  return result;
}

function sanitize(value) {
  return value.replace(/[\\/:*?"<>|\0]/g, '-').replace(/\s+/g, ' ').trim();
}

function timestamp() {
  const parts = new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,
  }).formatToParts(new Date()).reduce((acc, item) => {
    acc[item.type] = item.value;
    return acc;
  }, {});
  return `${parts.year}${parts.month}${parts.day}${parts.hour}${parts.minute}${parts.second}`;
}

function parseFile(value) {
  const splitAt = value.indexOf('=');
  if (splitAt <= 0) fail(`--file 格式错误：${value}`);
  const role = sanitize(value.slice(0, splitAt));
  const source = path.resolve(value.slice(splitAt + 1));
  if (!fs.existsSync(source) || !fs.statSync(source).isFile()) fail(`文件不存在：${source}`);
  return { role, source };
}

const args = parseArgs(process.argv.slice(2));
const endpoint = args.endpoint || process.env.PICGO_SERVER_URL || 'http://127.0.0.1:36677/upload';
const secret = String(process.env.PICGO_SERVER_SECRET || '').trim();
const stamp = timestamp();
const articleTitle = sanitize(args.articleTitle);
const files = args.files.map(parseFile);
const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'mp-article-picgo-'));

try {
  const staged = files.map((file) => {
    const extension = path.extname(file.source) || '.png';
    const uploadName = `${articleTitle}-${file.role}-${stamp}${extension}`;
    const uploadPath = path.join(tempDir, uploadName);
    fs.copyFileSync(file.source, uploadPath);
    return { ...file, uploadName, uploadPath };
  });

  if (args.dryRun) {
    console.log(JSON.stringify({ endpoint, dryRun: true, uploads: staged.map(({ uploadPath, ...item }) => item) }, null, 2));
  } else {
    const headers = { 'Content-Type': 'application/json' };
    if (secret) headers.Authorization = `Bearer ${secret}`;
    const response = await fetch(endpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify({ list: staged.map((item) => item.uploadPath) }),
    });
    const body = await response.text();
    if (!response.ok) fail(`PicGo 返回 HTTP ${response.status}：${body}`);

    let payload;
    try {
      payload = JSON.parse(body);
    } catch {
      fail(`PicGo 返回了无效 JSON：${body}`);
    }
    if (!payload.success || !Array.isArray(payload.result) || payload.result.length !== staged.length) {
      fail(`PicGo 返回数量与输入不一致：${body}`);
    }

    const uploads = staged.map((item, index) => ({
      role: item.role,
      source: item.source,
      uploadName: item.uploadName,
      url: payload.result[index],
    }));
    if (uploads.some((item) => !String(item.url).startsWith('https://'))) {
      fail('PicGo 返回了非 HTTPS 地址，停止更新文章引用');
    }

    console.log(JSON.stringify({ success: true, endpoint, uploads }, null, 2));
  }
} finally {
  fs.rmSync(tempDir, { recursive: true, force: true });
}
