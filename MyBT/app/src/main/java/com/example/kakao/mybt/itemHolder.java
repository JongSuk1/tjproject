package com.example.kakao.mybt;


import java.util.ArrayList;

public class itemHolder{
    private ArrayList<item> list_item;

    public ArrayList<item> getList_item() {
        return list_item;
    }


    public void setList_item(ArrayList<item> list_item) {
        this.list_item = list_item;
    }

    public void append_item(item item1){
        list_item.add(item1);
    }

    public itemHolder(){
        this.list_item = new ArrayList<item>();
    }

    private static final itemHolder holder = new itemHolder();

    public static itemHolder getInstance(){
        return holder;
    }

}
