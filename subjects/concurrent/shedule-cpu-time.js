// 分时操作

var show = console.log;

var queue = [];

var global_time;
var time_piece;

function getNowTime()
{
    // 获取当前时间戳，毫秒级
    return new Date().getTime();
}

function sleep(ms)
{
    // 阻塞型sleep，模拟给定时长的计算
    var timeout = getNowTime() + ms;
    while (getNowTime() < timeout)
    {
        // show("test sleeping");
    }
}

function checkTimeout()
{
    var timeout = global_time + time_piece;
    var now = getNowTime();

    if (now < timeout)
    {
        return false;
    }
    else
    {
        global_time = now;
        return true;
    }
}

function addTask(t)
{
    if (checkTimeout())
    {
        queue.push(t);
    }
    else
    {
        t();
    }
}

function task_loop()
{
    while (queue.length != 0)
    {
        var t = queue.shift();
        t();
    }
}

function sumC(n, k)
{
    show("sum:", n);
    sleep(20);

    if (n == 0)
    {
        return k(0);
    }
    else
    {
        addTask(() => sumC(n - 1, sumRes => k(n + sumRes)));
    }
}

function prodC(n, k)
{
    show("prod:", n);
    sleep(50);

    if (n == 1)
    {
        return k(1);
    }
    else
    {
        addTask(() => prodC(n - 1, prodRes => k(n * prodRes)));
    }
}


function runConcurrent()
{
    global_time = getNowTime();
    time_piece = 100;

    sumC(10, show);
    prodC(10, show);

    show("task loop ---------------")

    task_loop();
}

runConcurrent();  // sumC大概每执行5次，prodC会执行2次
