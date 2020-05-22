pragma solidity ^0.4.25;
pragma experimental ABIEncoderV2;
import "./Table.sol";

contract UserTempInfo{
    address private _owner;

    modifier onlyOwner{
        require(_owner==msg.sender,"Auth:only owner is authorized.");
        _;
    }

    constructor () public{
        _owner=msg.sender;
    }

    event createEvent(address owner,string tableName);

    event insertEvent(string userIdNo,string position,string temperature,int time);

    function create() public onlyOwner returns(int){
        TableFactory tf=TableFactory(0x1001);
        int count=tf.createTable("user_temp","user_id_no","position,temperature,time");
        emit createEvent(msg.sender,"user_temp");
        return count;
    }

    function insert(string userIdNo,string position,string temperature,int time) public
                            onlyOwner returns(int){
        TableFactory tf=TableFactory(0x1001);
        Table table=tf.openTable("user_temp");

        Entry entry=table.newEntry();
        entry.set("user_id_no",userIdNo);
        entry.set("position",position);
        entry.set("temperature",temperature);
        entry.set("time",time);

        int count=table.insert(userIdNo,entry);
        emit insertEvent(userIdNo,position,temperature,time);
        return count;
    }

    function select(string userIdNo) public view returns( string[], string[],int[]){
        TableFactory tf=TableFactory(0x1001);
        Table table=tf.openTable("user_temp");

        Condition condition=table.newCondition();
        condition.EQ("user_id_no",userIdNo);

        Entries entries=table.select(userIdNo,condition);

        string[] memory position_bytes_list = new string[](uint256(entries.size()));
        string[] memory temperature_bytes_list = new string[](uint256(entries.size()));
        int[] memory time_list = new int[](uint256(entries.size()));
        for(int i=0; i<entries.size(); ++i) {
            Entry entry = entries.get(i);
            position_bytes_list[uint256(i)] = entry.getString("position");
            temperature_bytes_list[uint256(i)] = entry.getString("temperature");
            time_list[uint256(i)] = entry.getInt("time");
        }

        return (position_bytes_list, temperature_bytes_list,time_list);



    }

    function selectLatest(string userIdNo) public view returns(string){
        TableFactory tf=TableFactory(0x1001);
        Table table=tf.openTable("user_temp");

        Condition condition=table.newCondition();
        condition.EQ("user_id_no",userIdNo);

        Entries entries=table.select(userIdNo,condition);


        if(entries.size()==0) return "no data";
        return entries.get(entries.size()-1).getString("temperature");


    }









}
