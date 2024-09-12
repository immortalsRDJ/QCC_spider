var cryptoJs = require('crypto-js')

var r = function (e, t) {
    var hmacSha512 = cryptoJs.HmacSHA512(e, t);
    return hmacSha512.toString()
};

var r1 = function () {
    var o = {
        "n": 20,
        "codes": {
            "0": "W",
            "1": "l",
            "2": "k",
            "3": "B",
            "4": "Q",
            "5": "g",
            "6": "f",
            "7": "i",
            "8": "i",
            "9": "r",
            "10": "v",
            "11": "6",
            "12": "A",
            "13": "K",
            "14": "N",
            "15": "k",
            "16": "4",
            "17": "L",
            "18": "1",
            "19": "8"
        }
    };
    for (var e = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase(), t = e + e, n = "", i = 0; i < t.length; ++i) {
        var a = t[i].charCodeAt() % o.n;
        n += o.codes[a]
    }
    return n
};

var s = function () {
    var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {}
        , t = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase()
        , n = JSON.stringify(e).toLowerCase();
    return r(t + n, r1(t)).toLowerCase().substr(8, 20)
};

var s1 = function () {
    var e = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {}
        , t = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : ""
        , n = (arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : "/").toLowerCase()
        , i = JSON.stringify(e).toLowerCase();
    return r(n + "pathString" + i + t, r1(n))
};

function main(t, par) {
    var i = s(t, par);
    var l = s1(t, par, 'f7d239d312096b665fd9e4a46e603592');
    return {key: i, value: l}
}

var t = '/api/search/searchmulti';
var par = {
    "searchKey": "北京首都机场动力能源有限公司",
    "pageIndex": 1,
    "pageSize": 20,
}
console.log(main(t,par))