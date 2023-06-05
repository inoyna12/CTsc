const send = (i, j) =>
new Promise((resolve) =>
setTimeout(() => {
console.log(`账号:${i},模拟ID:${j}`);
resolve(‘hello‘);
}, Math[‘round‘](Math[‘random‘]() * 10000))
);
const start = Date.now();
for (let i = 0; i < 50; i++) for (let j = 0; j < 5; j++) send(i, j);
console.log(`执行时间:${Date.now() - start}ms`);