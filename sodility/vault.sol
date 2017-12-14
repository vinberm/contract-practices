pragma solidity ^0.4.0;

contract Vault {
	

	//金库的拥有者
	address public owner;
	//总金额
	uint public totalAmount;

    event Deposit(address _from, uint _amount); 
    event Withdrawal(address _to, uint _amount);

    //取现
	struct Withdrawals
	{
		uint value;
		address to;
		uint withdrawalTime; 	//提交取现申请时间
		uint finalizationTime;  //可取现时间，1天后
	}

	//待取现项
	Withdrawals[] public pendingWithdrawals;

	function vault() {
		owner = msg.sender;
	}
	
	//充入金额
	function deposit(uint _value) {
	    Deposit(msg.sender, _value);
	    totalAmount += _value;
	}

	//请求取款
	function requestWithdrawal(uint _value, address _to) returns (uint){
	    if(msg.sender != owner)
	        throw;
		pendingWithdrawals.push(Withdrawals({
			value: _value,
			to: _to,
			withdrawalTime: now,
			finalizationTime: now + 86400
		}));
		return pendingWithdrawals.length - 1;
	}

	//取消取款
	function cancelWithdrawal(uint _index) returns (bool) {
	    if(msg.sender != owner)
	        throw;
		if(_index >= pendingWithdrawals.length){
			return false;
		}
		if(now >= pendingWithdrawals[_index].finalizationTime) {
			return false;
		}
		delete pendingWithdrawals[_index];
		return true;
	}

    //确认取款
	function confirmWithdrawal(uint _index) {
		if(_index >= pendingWithdrawals.length || now < pendingWithdrawals[_index].finalizationTime)
			throw;

        uint amount = pendingWithdrawals[_index].value;
        pendingWithdrawals[_index].value = 0;
	//发送金额到指定地址
	    address to = pendingWithdrawals[_index].to;
		if(!to.send(amount))
			throw;
		totalAmount -= amount;
		delete pendingWithdrawals[_index];
		Withdrawal(to, amount);

	}



}