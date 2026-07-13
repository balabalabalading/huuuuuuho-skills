import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import test from 'node:test';

const script = new URL('./upload-images-to-picgo.mjs', import.meta.url).pathname;
const skillRoot = path.resolve(path.dirname(script), '..');

function tempUploadDirs() {
  return new Set(fs.readdirSync(os.tmpdir()).filter((name) => name.startsWith('mp-article-picgo-')));
}

function makeImage() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'mp-article-test-'));
  const file = path.join(dir, 'cover.png');
  fs.writeFileSync(file, 'png');
  return { dir, file };
}

function runCli(args, env = {}) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, [script, ...args], {
      env: { ...process.env, ...env },
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => { stdout += chunk; });
    child.stderr.on('data', (chunk) => { stderr += chunk; });
    child.on('close', (code) => resolve({ code, stdout, stderr }));
  });
}

function startServer(handler) {
  return new Promise((resolve) => {
    const server = http.createServer(handler);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${port}` });
    });
  });
}

function stopServer(server) {
  return new Promise((resolve) => server.close(resolve));
}

test('dry-run 不访问网络并清理临时目录', async () => {
  const image = makeImage();
  const before = tempUploadDirs();
  try {
    const result = await runCli([
      '--article-title', '测试文章',
      '--endpoint', 'http://127.0.0.1:1',
      '--file', `封面=${image.file}`,
      '--dry-run',
    ]);
    assert.equal(result.code, 0, result.stderr);
    const output = JSON.parse(result.stdout);
    assert.equal(output.endpoint, 'http://127.0.0.1:1/upload');
    assert.equal(output.heartbeat, 'http://127.0.0.1:1/heartbeat');
    assert.deepEqual(tempUploadDirs(), before);
  } finally {
    fs.rmSync(image.dir, { recursive: true, force: true });
  }
});

test('自定义端口、基础地址和 Bearer secret 可以上传', async () => {
  const image = makeImage();
  const requests = [];
  const { server, baseUrl } = await startServer((request, response) => {
    requests.push({ url: request.url, auth: request.headers.authorization });
    response.setHeader('Content-Type', 'application/json');
    if (request.url === '/heartbeat') response.end(JSON.stringify({ success: true, result: 'alive' }));
    else response.end(JSON.stringify({ success: true, result: ['https://img.example.com/cover.png'] }));
  });
  try {
    const result = await runCli([
      '--article-title', '测试文章',
      '--endpoint', baseUrl,
      '--file', `封面=${image.file}`,
    ], { PICGO_SERVER_SECRET: 'token' });
    assert.equal(result.code, 0, result.stderr);
    assert.deepEqual(requests.map((item) => item.url), ['/heartbeat', '/upload']);
    assert.ok(requests.every((item) => item.auth === 'Bearer token'));
    assert.equal(JSON.parse(result.stdout).uploads[0].url, 'https://img.example.com/cover.png');
  } finally {
    await stopServer(server);
    fs.rmSync(image.dir, { recursive: true, force: true });
  }
});

test('完整 upload 地址不会重复追加路径', async () => {
  const image = makeImage();
  const paths = [];
  const { server, baseUrl } = await startServer((request, response) => {
    paths.push(request.url);
    response.setHeader('Content-Type', 'application/json');
    if (request.url === '/heartbeat') response.end(JSON.stringify({ success: true, result: 'alive' }));
    else response.end(JSON.stringify({ success: true, result: ['https://img.example.com/cover.png'] }));
  });
  try {
    const result = await runCli([
      '--article-title', '测试文章',
      '--endpoint', `${baseUrl}/upload`,
      '--file', `封面=${image.file}`,
    ]);
    assert.equal(result.code, 0, result.stderr);
    assert.deepEqual(paths, ['/heartbeat', '/upload']);
  } finally {
    await stopServer(server);
    fs.rmSync(image.dir, { recursive: true, force: true });
  }
});

test('旧版服务缺少 heartbeat 时继续上传', async () => {
  const image = makeImage();
  const { server, baseUrl } = await startServer((request, response) => {
    if (request.url === '/heartbeat') {
      response.statusCode = 404;
      response.end('not found');
      return;
    }
    response.setHeader('Content-Type', 'application/json');
    response.end(JSON.stringify({ success: true, result: ['https://img.example.com/cover.png'] }));
  });
  try {
    const result = await runCli([
      '--article-title', '测试文章',
      '--endpoint', baseUrl,
      '--file', `封面=${image.file}`,
    ]);
    assert.equal(result.code, 0, result.stderr);
    assert.match(result.stderr, /继续尝试上传接口/);
  } finally {
    await stopServer(server);
    fs.rmSync(image.dir, { recursive: true, force: true });
  }
});

test('401 返回 shared secret 指引', async () => {
  const image = makeImage();
  const { server, baseUrl } = await startServer((_request, response) => {
    response.statusCode = 401;
    response.end('Unauthorized');
  });
  try {
    const result = await runCli([
      '--article-title', '测试文章',
      '--endpoint', baseUrl,
      '--file', `封面=${image.file}`,
    ]);
    assert.equal(result.code, 1);
    assert.match(result.stderr, /PICGO_SERVER_SECRET/);
  } finally {
    await stopServer(server);
    fs.rmSync(image.dir, { recursive: true, force: true });
  }
});

test('连接失败和超时给出不同提示', async (t) => {
  const image = makeImage();
  await t.test('连接失败', async () => {
    const holder = await startServer((_request, response) => response.end());
    const closedUrl = holder.baseUrl;
    await stopServer(holder.server);
    const result = await runCli([
      '--article-title', '测试文章',
      '--endpoint', closedUrl,
      '--file', `封面=${image.file}`,
      '--timeout-ms', '200',
    ]);
    assert.equal(result.code, 1);
    assert.match(result.stderr, /连接失败/);
  });

  await t.test('请求超时', async () => {
    const { server, baseUrl } = await startServer(() => {});
    try {
      const result = await runCli([
        '--article-title', '测试文章',
        '--endpoint', baseUrl,
        '--file', `封面=${image.file}`,
        '--timeout-ms', '100',
      ]);
      assert.equal(result.code, 1);
      assert.match(result.stderr, /超时/);
    } finally {
      await stopServer(server);
    }
  });
  fs.rmSync(image.dir, { recursive: true, force: true });
});

test('返回数量异常和非 HTTPS 地址会阻止交付', async (t) => {
  const image = makeImage();
  await t.test('返回数量异常', async () => {
    const { server, baseUrl } = await startServer((request, response) => {
      response.setHeader('Content-Type', 'application/json');
      if (request.url === '/heartbeat') response.end(JSON.stringify({ success: true, result: 'alive' }));
      else response.end(JSON.stringify({ success: true, result: [] }));
    });
    try {
      const result = await runCli(['--article-title', '测试文章', '--endpoint', baseUrl, '--file', `封面=${image.file}`]);
      assert.equal(result.code, 1);
      assert.match(result.stderr, /返回数量与输入不一致/);
    } finally {
      await stopServer(server);
    }
  });

  await t.test('非 HTTPS 地址', async () => {
    const { server, baseUrl } = await startServer((request, response) => {
      response.setHeader('Content-Type', 'application/json');
      if (request.url === '/heartbeat') response.end(JSON.stringify({ success: true, result: 'alive' }));
      else response.end(JSON.stringify({ success: true, result: ['http://img.example.com/cover.png'] }));
    });
    try {
      const result = await runCli(['--article-title', '测试文章', '--endpoint', baseUrl, '--file', `封面=${image.file}`]);
      assert.equal(result.code, 1);
      assert.match(result.stderr, /非 HTTPS 地址/);
    } finally {
      await stopServer(server);
    }
  });
  fs.rmSync(image.dir, { recursive: true, force: true });
});

test('开源工作流默认本地模式并使用相对 Markdown 路径', () => {
  const skill = fs.readFileSync(path.join(skillRoot, 'SKILL.md'), 'utf8');
  const readme = fs.readFileSync(path.join(skillRoot, 'README.md'), 'utf8');
  assert.match(skill, /MP_ARTICLE_IMAGE_MODE/);
  assert.match(skill, /默认.*local/);
  assert.match(skill, /!\[中文说明\]\(article-assets\/<文章标识>\//);
  assert.match(readme, /Default.*local|默认.*local/);
});
