import JuejinHelper from "juejin-helper";
import schedule from "node-schedule";
let ck = {
    '识别标识（数字字母 建议用qq后面可能会更新qq机器人方式推送消息）': 'juejin.com的CK',
    '识别标识': 'juejin.com的CK',
    '识别标识': 'juejin.com的CK',
    '识别标识': 'juejin.com的CK',//多账户另起一行
}

export async function juejingames(e) {
    const juejin = new JuejinHelper();
    await juejin.login(ck[e.user_id]);
    const seagold = juejin.seagold();

   let signTime= setInterval(async() => {
        await seagold.gameLogin(); // 登陆游戏
        let gameInfo = null;
        const info = await seagold.gameInfo(); // 游戏状态
        if (info.gameStatus === 1) {
            gameInfo = info.gameInfo; // 继续游戏
        } else {
            gameInfo = await seagold.gameStart(); // 开始游戏
        }
        const command = ["U", "L"];
        await seagold.gameCommand(gameInfo.gameId, command); // 执行命令
        const result = await seagold.gameOver(); // 游戏结束
        console.log(`本次游戏结束获得${result.gameDiamond}矿石,今日上限${result.todayLimitDiamond},今日以获取${result.todayDiamond} ${result.todayDiamond==result.todayLimitDiamond?'今日获取已达上限运行结束':'等待下一次运行'}`); // => { ... }
        if(result.todayDiamond==result.todayLimitDiamond){
            clearInterval(signTime)
            juejin.logout();
        }
    }, 12000)
    
}
export async function auto(e) {
    const juejin = new JuejinHelper();
    await juejin.login(ck[e.user_id]);
    const growth = juejin.growth();
    try {
        let res = await growth.checkIn()
        let resp = await growth.getCurrentPoint();
        // 抽奖
        await growth.drawLottery();
        console.log(`签到成功!剩余矿石${resp}`);
        await juejin.logout();
    } catch (error) {
        let resp = await growth.getCurrentPoint();
        let msg = [error.message, `当前剩余${resp}个矿石`]
        console.log(msg);
        await growth.drawLottery();
        await juejin.logout();
    }
    return true; //返回true 阻挡消息不再往下
}
//cron表达式 分别是 0秒 十分 0时 每天 大概就是这个意思 0 10 0 * * ?   
console.log(`启动成功,将在凌晨0:10分开始运行 首次运行请检查app.js是否配置ck`);
schedule.scheduleJob("0 10 0 * * ?", () => {
    console.log(`运行中将在凌晨0:10分开始运行`);
    for (const key in ck) {
        auto({ user_id: key })
        juejingames({ user_id: key })
    }
});
