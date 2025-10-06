const CryptoJS = require('crypto-js');
const got = require('got');
const cheerio = require('cheerio');
const qs = require('qs');
const USER = "inoyna", PASSWORD = "inoyna11";
class proxy {
    constructor() {
        this.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.51daili.com',
            'Referer': 'https://www.51daili.com/',
        };
    }
    async main() {
        await this.getcookies();
        await this.login();
        await this.signin();
    }
    async wait(ms) {
        await new Promise(resolve => setTimeout(resolve, ms));
    }
    async signin() {
        return new Promise((resolve) => {
            let opts = {
                url: "https://www.51daili.com/index/user/signin.html",
                method: "GET",
                headers: this.headers,
            }
            this.request(opts, (err, resp, data) => {
                try {
                    if (err) {
                        console.log(err)
                    } else {
                        console.log(JSON.stringify(data));
                    }
                } catch (e) {
                    console.log(e)
                } finally {
                    resolve(data);
                }
            });
        });
    }
    async login() {
        return new Promise((resolve) => {
            let opts = {
                url: "https://www.51daili.com/index/user/login.html",
                body: qs.stringify({
                    __login_token__: this.logintoken,
                    account: USER,
                    password: PASSWORD,
                    ticket: 1,
                    keeplogin: 1,
                    is_read: 1
                }),
                headers: this.headers,
                followRedirect: false
            }
            this.request(opts, (err, resp, data) => {
                try {
                    if (err) {
                        console.log(err)
                    } else {
                        if (data.code === 1) {
                            console.log("登录成功");
                            this.headers.Cookie = (this.headers.Cookie || "")
                                .split(";")
                                .filter((x) => !x.trim().startsWith("tncode_check="))
                                .join(";");
                            const newCookies = resp.headers["set-cookie"]
                                .map((x) => x.split(";")[0])
                                .filter((x) => !x.startsWith("tncode_check="))
                                .join(";");
                            this.headers.Cookie = newCookies
                                ? (this.headers.Cookie ? this.headers.Cookie + "; " + newCookies : newCookies)
                                : this.headers.Cookie;
                        } else {
                            console.log(`登录失败，原因：${JSON.stringify(data)}`);
                        }
                    }
                } catch (e) {
                    console.log(e)
                } finally {
                    resolve(data);
                }
            });
        });
    }
    async getcookies() {
        return new Promise((resolve) => {
            let opts = {
                url: "https://www.51daili.com",
                method: "GET",
                headers: this.headers,
                followRedirect: false,

            }
            this.request(opts, (err, resp, data) => {
                try {
                    if (err) {
                        console.log(err)
                    } else {
                        const $ = cheerio.load(data);
                        this.logintoken = $('input[name="__login_token__"]').val();
                        this.headers.Cookie = resp.headers["set-cookie"]
                            .map((x) => x.split(";")[0])
                            .join(";") + "; tncode_check=ok";
                    }
                } catch (e) {
                    console.log(e)
                } finally {
                    resolve(data);
                }
            });
        });
    }
    request(params, callback) {
        const { url, method = 'POST', ...others } = params;
        got(url, { method, ...others }).then(
            (res) => {
                let body = res.body;
                try {
                    body = JSON.parse(body);
                } catch (error) { }
                callback(null, res, body);
            },
            (err) => {
                callback(err?.response?.body || err);
            }
        );
    }
}

(async () => {
    await new proxy().main();
})();
