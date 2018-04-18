package com.example.kakao.mybt;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Intent;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;
public class feedActivity extends AppCompatActivity {

    private Button sBack; // s for 'sub'
    private ListView sListView;
    private TextView sTextView;

    private itemHolder s_itemHolder;
    private ArrayList<item> slist_item;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_feed);


        MyImageAdapter sImageAdapter;
        s_itemHolder = itemHolder.getInstance();
        slist_item = s_itemHolder.getList_item();

        sTextView = (TextView) findViewById(R.id.msg_textview);

        sListView = (ListView) findViewById(R.id.feedListview);
        if(slist_item != null){
            sTextView.setText("image");
            sImageAdapter = new MyImageAdapter(this, slist_item);
            sListView.setAdapter(sImageAdapter);
        }
        else{
            sTextView.setText("no such image");
        }



    }
}
