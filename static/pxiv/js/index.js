var app = new Vue({
    el: '#app',
    data: {
        imgData: "",
        hitoko: 'Hello!',
        author:'',
    },
    mounted() {
        this.getData()
    },

    methods: {
        getData() {
            console.log("2333")
            fetch('/pxiv/getData',
                {
                    method: 'POST',
                    credentials: "same-origin",
                    headers: {
                        'Accept': 'application/json, text/plain, */*',
                        'Content-Type': 'application/json',
                    },
                    //请求的参数
                    //body: JSON.stringify(this.saveStoreWish)
                }).then((response) => {
                /*判断请求状态码*/
                if (response.status !== 200) {
                    console.log("请求失败，状态码为：" + response.status);
                    return;
                } else {
                    return response.json();
                }
            }).then((json) => {
                if (json['status'] == true) {
                    //this.openTopPopup(1, json['msg']);
                    this.imgData = "data:image/jpeg;base64,"+json['data']['imgData'];
                    this.author = json['data']['hitoko']['author'];
                    this.hitoko = json['data']['hitoko']['hitokoto'];
                    console.log(json['msg']);

                } else {
                    //this.openTopPopup(0, json['msg']);
                    console.log(json['msg'])
                }
            }).catch((err) => {
                console.log("请求pxiv/getData失败：" + err);
            });
        },
        //查询验证码
        search() {
            if ((this.mobile !== null) && (checkMobile(this.mobile))) {
                fetch('/hop/search?mobile=' + this.mobile + '&env=' + this.env, {
                    method: 'get'
                }).then((response) => {
                    return response.json();
                }).then((json) => {
                    this.code = json['data'];
                    this.code = json['data'];
                }).catch((err) => {
                    console.log(err)
                });
            } else {
                alert("请输入正确手机号");
            }
        },
    },
});