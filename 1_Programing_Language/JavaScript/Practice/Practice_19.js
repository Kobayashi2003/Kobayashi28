function type(target) {
    // 原始值 引用值
    // 区分引用值
    var template = {
        "[object Array]" : "array",
        "[object Object]" : "object",
        "[object Number]" : "number - object",
        "[object Boolean]" : "bollen - object",
        "[object String]" : "string - object"
    };

    if(typeof(target) === null) {
        return null;
    }
    else if(typeof(target) == "object") {
        var str = Object.prototype.toString.call(target);
        return template[str];
    }
    else {
        return typeof(target);
    }
}
