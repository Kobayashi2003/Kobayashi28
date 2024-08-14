function stack() {
    var type = {
        Number : "",
        String : "",
        Boolean : "",
        Undefined : 0,
        Null : 0,
        Funciton : "",
        Object : "",
    };
    var obj = {
        push: function (data) {
            result = typeof (data);
            if (result === "number") {
                type.Number += data + " ";
            }
            else if (result === "string") {
                type.String += data + " ";
            }
            else if (result === "boolean") {
                type.Boolean += data + " ";
            }
            else if (result === "undefined") {
                type.Undefined++;
            }
            else if (result === "null") {
                type.Null++;
            }
            else if (result === "function") {
                type.Funciton += data + "</br>";
            }
            else if (result === "object") {
                type.Object += data + "</br>";
            }
            else {
                console.log("WRONG!!");
                return;
            }
        },
        pop : function (message) {
            if (message === "number") {
                console.log(type.Number);
            }
            else if (message === "string") {
                console.log(type.String);
            }
            else if (message === "boolean") {
                console.log(type.Boolean);
            }
            else if (message === "undefined") {
                console.log(type.Undefined);
            }
            else if (message === "null") {
                console.log(type.Null);
            }
            else if (message === "function") {
                console.log(type.Funciton);
            }
            else if (message === "object") {
                console.log(type.Object);
            }
            else {
                console.log("WRONG!!");
                return;
            }
        },
        refresh : function() {
            type.Number = type.String = type.Boolean = "";
            type.Undefined = type.Null = 0;
            type.Function = type.Object = "";
        }
    }
    return obj;
}
var fun = stack();