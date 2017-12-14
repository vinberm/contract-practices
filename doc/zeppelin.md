# zeppelin

## 简介
OpenZeppelin是一个安全地编写以太坊上智能合约的代码库。


## 安装
- OpenZeppelin可以集成在[Truffle](https://github.com/trufflesuite/truffle)中，首先安装Truffle。
```
npm install -g truffle
mkdir myproject && cd myproject
truffle init
```

- 再安装OpenZeppelin库，运行如下命令：
```
npm init
npm install zeppelin-solidity
```

- 这时合约库代码在 `node_modules/zeppelin-solidity/contracts中`，可以调用代码：
```
import 'zeppelin-solidity/contracts/ownership/Ownable.sol';
contract MyContract is Ownable {
	...
}
```

## 常用合约库
OpenZeppelin提供安全、经过测试与社区审计过的代码，代码实现见[zeppelin-github](https://github.com/OpenZeppelin/zeppelin-solidity)，这里列举几个，更多见文档[zeppelin-readthedocs](http://zeppelin-solidity.readthedocs.io/en/latest/)

### Ownable

- Ownable()
设置合约创建者的地址为owner。

- modifier onlyOwner()
只有owner可以调用函数，阻止其他人调用。

- transferOwnership(address newOwner) onlyOwner
将owner转移给其他地址，只有owner可以调用该函数。

### Claimable
Ownable合约的一个扩展，所有权需要先声明

- transfer(address newOwner) onlyOwner
设置传入地址为待定的owner

- modifier onlyPendingOwner
表示该函数只能由待定的owner调用

- claimOwnership() onlyPendingOwner
完成所有权的转让，将待定的owner专为新的（正式的）owner


### Migrations
基础合约，允许用一个不同的地址代表自己新的实例。继承Ownable合约。

- upgrade(address new_address) onlyOwner
依据传入的地址，创建一个新的合约实例

- setCompleted(uint completed) onlyOwner
设置迁移完成的时间

### SafeMath
提供经过安全检查的数学操作函数

- assert(bool assertion) internal
检查数学表达式，如果传递的结果是false，则抛出错误。

- mul(uint256 a, uint256 b) internal returns(uint256)
两个无符号整数相乘，检查乘积除以非零被乘数等于乘数。

- sub(uint256 a, uint256 b) internal returns(uint256)
两个无符号整数相减，相减前检查b不大于a。

- add(uint256 a, uint256 b) internal returns(uint256)
两个无符号整数相加，检查结果大于a且大于b。


### LimitBalance
基础合约，限制一个合约能够拥有资金的数量。

- LimitBalance(uint _limit)
构造函数，根据传入的无符号整数，限制这个合约拥有的资金量。

- modifier limitedPayable()
如果合约余额超过限制，抛出错误。


### PullPayment
基础合约。继承该合约，可异步转账。相当于付款人先把资金先保管在合约中，收款人再从合约中取现。

- asyncSend(address dest, uint amount) internal
该函数由付款人调用，将可用数量的金额转入目的地址。

- withdrawPayments()
当付款人调用该合约函数，则发送指定余额给付款人。如果指定余额为0、合约没有足够资金或者交易失败，那么就抛出错误。


### StandardToken

- approve(address _spender, uint _value) returns(bool success)
设置传入的地址允许使用发送人拥有的币余额的数量。

- allowance(address _owner, address _spender) constant returns(uint remaining)
返回spender可以使用owner余额的数量。

- balanceOf(address _owner) constant returns(uint balance)
返回传入地址拥有的币的余额。

- transferFrom(address _from, address _to, uint _value) returns(bool success)
从发送人允许转币的账户转移一定数量的币，其中币的数量不能大于被允许的数目，并且不能超过_from账户的余额.

- transfer(address _to, uint _value) returns(bool success)
从发送人账户转币，数量不能不大于发送人账户的余额。


## Security audits
另外，Zeppelin为组织提供私有或公有代码审计。检阅合约或应用代码，并写一个含有发现的问题的报告。他们主要审计关于Solidity、EVM assembly、JavaScript、Python和Bitcoin Scripting code。


## 合约代码注意事项
- 避免使用var声明变量。
- 避免在循环里执行复杂计算，因为gas耗完会回滚，但是费用还是支付了。
- 简单、模块化
