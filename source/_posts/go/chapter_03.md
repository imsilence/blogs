title: GO顺序编程
date: 2015-09-20 12:10:21
tags: [golang]
categories: [开发语言]
---

## 变量 ##
变量可以认为是程序在内存中申请一块数据存储空间的名称, 程序常常声明一个变量, 然后再内存中申请一块空间, 将内存空间指向变量

+ 变量声明
go语言使用var关键字声明一个变量, 格式: `var var_name var_type`
```
var _i_var int
var _s_var string
var _iarr_var [32]int
var _lslice_var []long
var _struct_var struct {
    _i_var int
}
var _p_var *int
var _map_var [string]int
var _func_var func(args int) int
```
可以使用var定义多个变量: 
```
var (
    _i_var int
    _s_var string
)
```

+ 变量初始化&赋值
可以在声明变量时进行初始化操作, 也可以在声明后对变量进行赋值
```
var _i1_var int = 10
var _i2_var = 10
_i3_var := 10
```
说明:
1. 以上三种方式均为在声明变量时进行初始化, 因为在go是强类型语言, 因此在初始化时可以推测出数据类型所以使用声明并赋值的时可以省略类型的定义
2. 使用`:=`明确表示此处为声明变量并初始化, 操作符前的变量不能被声明

```
var _i4_var int
_i4_var = 10

var (
    _i5_var int
    _i6_var int
)
_i5_var, _i6_var = 11, 12

_i5_var, _i6_var = _i6_var, _i5_var

fmt.Println("i5:", _i5_var, "i6:", _i6_var)
```
说明:
1. 以上两种方式均为先声明变量 在进行赋值
2. go支持多重赋值操作, 当然也支持像Python那么强大的变量交换

+ 匿名变量
在某个时候接收函数返回的多个变量时, 可能只关注某个或某几个变量, 此时可以使用"_"接收不关注的变量
```
func get_name() (firstname, lastname) {
    return "uk", "silence"
}

_, lastname := get_name()
```

## 常量 ##
常量表示在编译时已经知道且不可改变的值, 包括整型、浮点型、复数型、布尔型、字符串型等

+ 字面常量
指硬编码在代码中的常量

+ 常量定义
通过const来定义一个常量
```
const pi float64 = 3.1415926
const zero = 0.0

const (
    size int64 = 1024
    eof = -1
)

const a, b, c = 1, 1.1, "test"
```

常量可以指定类型也可以不指定类型, 在不指定类型时为无类型常量, 常量的右操作数不可以是在运行期得到的结果，必须为编译期已知的值

+ 预定义常量
go中预定义了true, false和iota

iota表示在编译期修改的常数, 当iota第一次出现时为0, 每出现一次iota变量加1

```
const (
    c0 = 1 << iota    // c0 = 1
    c1 = 1 << iota    // c1 = 2
    c2 = 1 << iota    // c2 = 4
)

const (
    c0 = 1 << iota
    c1
    c2
)

const (
    Sunday = iota
    Monday
    Tuesday
    Wednesday
    Thursday
    Firday
    Saturday
    numberOfDays    //注意此处变量名开头为小写, 表示对外(package)不可见
)
```

说明:
1. 在const中两个赋值表达式一样可以省了后一个，因此以上两种方式结果是一样的
2. go中未提供enum关键字用来定义枚举类型, 但是可以使用const+iota来实现
3. 在go中使用命名约定表示变量对外的权限, 大写表示对外可见, 小写表示对外不可见

## 数据类型 ##
go中的基本数据类型有:
+ 布尔类型: bool
使用关键字bool定义布尔类型, 只接收true, false两个值, 不支持其他类型转换
```
var _is_alive = true

var _is_equals = (1 == 1)

var _is_empty = bool('')    //error

fmt.Println("is Alive:", _is_alive)
```

+ 整数类型:
go支持的整数类型有:

|类型|字节长度|值范围|
|----|--------|------|
|int8|1|-128 ~ 127|
|uint8(byte)|1|0-255|
|int16|2|-32768 ~ 32767|
|uint16|2|0-65535|
|int32|4|-2147483648 ~ 2147483647|
|uint32|4|0 ~ 4294967296|
|int64|8|-9223372036854775808 ~  9223372036854775807|
|uint64|8|0 ~ 18446744073709551616|
|int|平台相关|平台相关|
|uint|平台相关|平台相关|
|uintptr|同指针|在32位系统为4字节, 64位系统为8字节|

说明:
1. 为避免程序移植问题在常规开发中使用int, uint, uintptr
2. 不同类型数据转化, 必须使用关键字强制转化, 需要注意数据截断造成的数据溢出和精度问题
3. 在使用":="初始化整数类型时默认为int类型
4. 数值运算支持 +, -, *, /, %
5. 比较运算支持 ==, !=, >, >=, <, <=, 注意两个不同数据类型的变量不能进行比较, 但是可以和字面常量比较
6. 位操作符支持 |, &, ~, ^, <<, >>

+ 浮点类型: float32, float64
浮点类型用于表示有小数点的不准确的数值类型
1. go定义了两种浮点类型float32和float64
2. 在使用":="初始化浮点类型时默认为float64类型
3. 在使用关键字强制转化浮点数类型时，需要注意截断和数据溢出问题
4. 因为浮点型为非精确的数值，因此在等于比较时应使用在一定误差范围内近似等于

+ 复数类型: complex64, complex128
复数表示由两个实数分别表示实部和虚部组成
```
var point complex64 = 32 + 64.0i

fmt.Println(point, real(point), imag(point))
```
1. complex64表示由两个float32组成复数, complex128自然对应float64组成的复数
2. 可以使用real和image分别获取复数的实部和虚部

+ 字符串类型: string
```
var name string = "silence"

fc := name[0]

fmt.Printfln("my name is %s, length %s, the first character is %s", name, len(name), fc)
```

1. 可以通过索引访问字符串内字符, 但不可以通过索引进行修改
2. 可以通过len方法获取字符串占字节长度
3. go中只支持utf-8和unicode两种编码
4. 可以使用连接符+, 将两个字符串连接为一个新的字符串
5. 字符串比遍历
go支持两种字符串遍历方式, 一种使用字节数组方式, 一种以unicode字符遍历
```
cxt = "Hello, 世界!"
_length = len(cxt)
for i := 0; i < _length; _length++ {
    ch := cxt[i]
    fmt.Println(i, ch)
}
for i, ch := range cxt {
    fmt.Println(i, ch)
}
```
unicode字符宝石遍历时每个字符类型为rune

+ 字符类型: rune
go支持两种字符类型, 一种为byte表示utf-8字符串的单个字节值, 一个是rune，表似单个unicode字符

+ 错误类型: error

go中符合数据类型有:
+ 指针类型: pointer
+ 数组类型: array
表示一系列相同类型数据的集合
```
[32]byte                    //长度为32, 每个元素为一个字节
[2*N] struct {x, y int32}   //复杂类型数组
[1000]*float64              //定义指针数组
[3][5]int                   //二位数组
[2][3][4]float64            //多维数组
```
1. 数组长度定义后不可修改, 可以在声明长度时使用常量或常量表达式, 数组的长度为数组类型的一个内置常量通过len函数获取数组长度
2. 通过索引访问数组元素，可以使用索引和range两种方式遍历数组元素
```
_len = len(array)
for i := 0; i < _len; i++ {
    fmt.Println(i, array[i])
}

for i, v := range array {
    fmt.Println(i, v)
}
```
3. go中数组类型为一种值类型, 表示在变量赋值时将发生数组复制

+ 切片: slice
切片主要用于弥补数组的缺陷, 数组切片可以抽象为:
1. 一个指向原生的数组的指针
2. 数组切片中的元素个数
3. 数组切片已经分配的存储 
切片的操作:
1. 创建
可以通过数组或者直使用make函数接创建切片
```
var _arr [5]int = [5]int{1, 2, 3, 4, 5}
var _slice_1 []int = _arr[:2]

var _slice_2 []int = _arr[2:]
var _slice_3 []int = _arr[:]

_slice_5 := make([]int, 5)          //创建5个元素初始值为0数组切片
_slice_6 := make([]int, 5, 10)      //创建5个元素初始值为0数组切片, 并预留10个的存储空间
_slice_7 := []int{1, 2, 3, 4, 5}    //创建5个元素切片, 此时也会创建一个匿名数组
```
2. 切片的遍历操作数组相同
3. 动态增减元素
go提供cap函数和len函数分别获取切片分配的空间大小和已存储的元素个数
可使用append函数将不定个参数追加到切片后并返回一个新的数组切片，可一个使用将数组切片追加到另一个切片后
```
slice_2 = append(slice_1, 1, 2, 3)
slice_3 := []int{8, 9, 10}
slice_4 = append(slice_2, slice_3...)
```
4. 基于数组切片创建数组切片
```
slice_1 := []int{8, 9, 10}
slice_2 := slice_1[:2]
```
5.内容复制
可以使用copy函数将一个数组切片赋值到另一个数组切片, 若两个切片大小不同, 则使用最小的数组切片的长度进行复制

+ 字典: map
map是一堆键值对的未排序集合
```
var users map[string] User
users = make(map[string] User)

users["1"] = User{"1", "test1"}
users["2"] = User{"2", "test2"}

user, _ok := users["12"]
if _ok {
    fmt.Println(user.Name)
} else {
    fmt.Println("not found")
}
```
1. 声明: `var name map[key_type] value_type`
2. 创建: 使用make来创建一个新的map, `make(map[key_type] value_type, length)`
创建一个初始存储为length的map
可以创建时并对map进行初始化:
```
users = map[string] User {
    "1": User{"1", "test1"},
    "2": User{"2", "test2"}
}
```
3. 可以通过key对map进行赋值
4. 可以通过delete方法删除map内的元素: `delete(map, key)`
5. 读取操作, 通过key读取map的值时会返回两个值, 第二个值表示十分读取到, 若读取到则第一个值表示读取的值


+ 通道: chan
+ 结构体: struct
+ 接口: interface

## 流程控制 ##
go语句支持条件, 选择, 循环, 跳转四种语句和扩展的关键字break, continue fallthrough
+ 选择: if, else, else if
```
var _i int = 23

if i > 32 {
    fmt.Println('gt 32')
} else {
    fmt.Println('lte 32')
}
```

+ 选择: switch, case, select
```
var _i int = 2
switch i {
    case 1:
        fmt.Println('one')
    case 2:
        fmt.Println('two')
    case 3:
        fallthrough
    case 4:
        fmt.Println('three four')
    case 5, 6, 7:
        fmt.Println('five six seven')
    default:
        fmt.Println('other')
}

switch {
    case _i < 5:
        fmt.Println('lt 5')
    case _i == 5:
        fmt.Println('eq 5')
    case default:
        fmt.Println('gt 5')
}
```

+ 循环: for, range
```
for i :=0; i < num; i++ {
    fmt.Println(i)
}

num := 0
for {
    num++
    if num >= 10 {
        break
    }
}
```

break后可标签, 表示跳转到标签定义同层的for循环外

+ 跳转: goto
同c语言的goto, 可以指定跳转到任意位置

## 函数 ##
函数由func关键字, 函数名, 参数, 返回值, 函数体, 返回语句组成
函数定义:
```
package mmath
import "errors"

func Madd(a, b int) (ret int, err error) {
    if a < 0 || b < 0 {
        err = errors.New("shoud be non-negative numbers")
        return
    }
    return a + b, nil
}

func Mnegate(a int) int {
    return -a
}

```
函数调用:
```
import "mmath"

c := mmath.Madd(1, 2)
```
说明:
1. 若连续若干个参数的类型相同, 可只保留最后一个参数的类型
2. 若返回值只有一个则可以省略参数名和括号
3. 函数名字为小写表示在本包中访问, 大小表示在包外可以访问
4. 在参数中可以使用不定参数
```
func PrintArgs(args ...int) {
    for _, v := range args {
        fmt.Println(v)
    }
    PrintArgs2(args...)
}

func PrintArgs2(args ...int) {
    for _, v := range args {
        fmt.Println(v)
    }
}
```
说明:
a. 在函数顶定义时使用...type 表示不定参数, 这些参数类型必须相同, 既有固定的参数又有可变参数时，可变参数放在最后
b. 可变参数可以向下传递, 使用args...
5. 任意类型的不定参数
```
func PrintArgs3(args ...interface{}) {
    for _, arg := range args {
        switch arg.(type) {
            case int:
                fmt.Println(arg, "is int")
            case string:
                fmt.Println(arg, "is string")
            default:
                fmt.Println(arg, "is other")
        }
    }
}

PrintArgs3(1, "2", 5.0)           
```

6.匿名函数&闭包
go可以在任意位置定义匿名函数并赋值给某个变量

```
genrate_factory := func() (func()) {
    var _id int = 0
    //return func() int {
    return func() {
        _id += 1
        fmt.Println(_id)
        //return _id
    }
}
g1 := genrate_factory()
//fmt.Println(g1())
g1()
```

7.错误处理
在go中定义error接口来进行错误处理
函数定义:
```
func func_name(args ...interface{}) (rt type, err error) {
    
}
```
调用:
```
rt err := func_name()
if err != nil {
    //正确处理   
}
```

自定义错误类型:
```
type MyError struct {
    err error
    text string
}

func (e *MyError) Error() string {
    return e.text + " " + e.err.Error()
}
func test_error(a int) (rt int, err error) {
    if a == 0 {
        return 0, &MyError{errors.New(""), "zero"}
    }
    return a, nil
}

func main() {
    _rt, err := test_error(0)
    if err == nil {
        fmt.Println(_rt)
    } else {
        fmt.Println(err)
    }
}

```

8. defer关键字
使用java或python的同学比较熟悉, 类似于在发生不管是否发生异常在函数执行完成后执行finally体内的代码

```
defer func() {
   //清理函数 
}()
```

9. panic, recover
go提供函数painic和recover报告和处理运行时错误和程序中错误:
```
func panic(interface{})
func recover() interface{}
```
到调用panic函数后，函数执行将终止返回到函数, 并依次逐层执行panic知道goroutine中所有正在的函数被终止, 错误信息通过panic的参数传递
```
panic(404)
panic(Erro("file not found"))
```
recover函数用于终止错误，一般情况下, recover应该在一个使用defer关键字的函数中执行已有效截取错误处理, 若在没有发生异常的gorouting中明确调用recover将导致该gorouting所属进程打印异常信息并直接退出
```
def func() {
    if r := recover(); r != nil {
        log.Printf("Runtime error:%v", r)
    }
} ()
```

panic类似于java或python中的抛出异常关键字throw和raise
recover类似于java或python中捕获异常的关键字catch和except
