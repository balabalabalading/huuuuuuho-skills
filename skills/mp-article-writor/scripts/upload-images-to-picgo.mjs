#!/usr/bin/env node

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const DEFAULT_SERVER_URL = 'http://127.0.0.1:36677';
const DEFAULT_TIMEOUT_MS = 10_000;

class CliError extends Error {}

function fail(message) {
  throw new CliError(message);
}

function parsePositiveInteger(value, label) {
  const parsed = Number.parseInt(value, 10);
  if (!Number.isFinite(parsed) || parsed <= 0) fail(`${label} 必须是正整数`);
  return parsed;
}

function parseArgs(argv) {
  const result = { files: [], dryRun: false };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--article-title') result.articleTitle = argv[++index];
    else if (arg === '--endpoint') result.endpoint = argv[++index];
    else if (arg === '--file') result.files.push(argv[++index]);
    else if (arg === '--timeout-ms') result.timeoutMs = argv[++index];
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

function resolveEndpoints(value) {
  const raw = value || process.env.PICGO_SERVER_URL || DEFAULT_SERVER_URL;
  let upload;
  try {
    upload = new URL(raw);
  } catch {
    fail(`PicGo Server 地址无效：${raw}`);
  }
  if (!['http:', 'https:'].includes(upload.protocol)) {
    fail(`PicGo Server 只支持 http 或 https：${raw}`);
  }

  const cleanPath = upload.pathname.replace(/\/+$/, '');
  upload.pathname = cleanPath.endsWith('/upload') ? cleanPath : `${cleanPath}/upload`;
  upload.pathname = upload.pathname.replace(/^\/\//, '/');

  const heartbeat = new URL(upload);
  heartbeat.pathname = upload.pathname.replace(/\/upload$/, '/heartbeat');
  return { upload: upload.toString(), heartbeat: heartbeat.toString() };
}

async function requestWithTimeout(url, options, timeoutMs, label) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } catch (error) {
    if (error?.name === 'AbortError') fail(`${label}超时，${timeoutMs}ms 内没有响应：${url}`);
    fail(`${label}连接失败，请检查 PicGo 是否启动、端口是否正确：${url}，${error.message}`);
  } finally {
    clearTimeout(timer);
  }
}

function authHeaders(secret, includeJson = false) {
  const headers = {};
  if (includeJson) headers['Content-Type'] = 'application/json';
  if (secret) headers.Authorization = `Bearer ${secret}`;
  return headers;
}

async function checkHeartbeat(endpoint, secret, timeoutMs) {
  const response = await requestWithTimeout(endpoint, {
    method: 'POST',
    headers: authHeaders(secret),
  }, timeoutMs, 'PicGo heartbeat ');

  if (response.status === 401) {
    fail('PicGo heartbeat 鉴权失败，服务启用了 shared secret，请设置 PICGO_SERVER_SECRET');
  }
  if (response.status === 404 || response.status === 405) {
    console.error(`PicGo heartbeat 不可用，继续尝试上传接口：HTTP ${response.status}`);
    return 'unsupported';
  }
  if (!response.ok) fail(`PicGo heartbeat 失败：HTTP ${response.status}`);
  return 'alive';
}

async function uploadFiles(endpoint, secret, staged, timeoutMs) {
  const response = await requestWithTimeout(endpoint, {
    method: 'POST',
    headers: authHeaders(secret, true),
    body: JSON.stringify({ list: staged.map((item) => item.uploadPath) }),
  }, timeoutMs, 'PicGo 上传 ');
  const body = await response.text();

  if (response.status === 401) {
    fail('PicGo 上传鉴权失败，服务启用了 shared secret，请设置 PICGO_SERVER_SECRET');
  }
  if (!response.ok) fail(`PicGo 上传失败：HTTP ${response.status}，${body}`);

  let payload;
  try {
    payload = JSON.parse(body);
  } catch {
    fail(`PicGo 返回了无效 JSON：${body}`);
  }
  if (!payload.success || !Array.isArray(payload.result)) {
    fail(`PicGo 返回格式异常：${body}`);
  }
  if (payload.result.length !== staged.length) {
    fail(`PicGo 返回数量与输入不一致，输入 ${staged.length}，返回 ${payload.result.length}`);
  }
  return payload.result;
}

async function main() {
  if (Number.parseInt(process.versions.node.split('.')[0], 10) < 18) {
    fail(`需要 Node.js 18 或更高版本，当前版本为 ${process.versions.node}`);
  }

  const args = parseArgs(process.argv.slice(2));
  const endpoints = resolveEndpoints(args.endpoint);
  const timeoutMs = parsePositiveInteger(
    args.timeoutMs || process.env.PICGO_REQUEST_TIMEOUT_MS || DEFAULT_TIMEOUT_MS,
    '请求超时',
  );
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
      console.log(JSON.stringify({
        mode: 'picgo',
        dryRun: true,
        endpoint: endpoints.upload,
        heartbeat: endpoints.heartbeat,
        uploads: staged.map(({ uploadPath, ...item }) => item),
      }, null, 2));
      return;
    }

    const heartbeat = await checkHeartbeat(endpoints.heartbeat, secret, timeoutMs);
    const urls = await uploadFiles(endpoints.upload, secret, staged, timeoutMs);
    const uploads = staged.map((item, index) => ({
      role: item.role,
      source: item.source,
      uploadName: item.uploadName,
      url: urls[index],
    }));
    if (uploads.some((item) => !String(item.url).startsWith('https://'))) {
      fail('PicGo 返回了非 HTTPS 地址，公众号无法可靠加载，停止更新文章引用');
    }

    console.log(JSON.stringify({
      success: true,
      mode: 'picgo',
      endpoint: endpoints.upload,
      heartbeat,
      uploads,
    }, null, 2));
  } finally {
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error instanceof CliError ? error.message : error.stack || error.message);
  process.exitCode = 1;
});
