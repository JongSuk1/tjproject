package com.example.kakao.mybt;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;

/**
 * Created by kakao on 2018. 4. 13..
 */

public class MyImageAdapter extends BaseAdapter {

    Context context;
    ArrayList<item> list_itemArrayList;

    ImageView capturedImageView;
    TextView title;

    public MyImageAdapter(Context context, ArrayList<item> list_itemArrayList) {
        this.context = context;
        this.list_itemArrayList = list_itemArrayList;
    }

    @Override
    public int getCount() {
        return this.list_itemArrayList.size();
    }

    @Override
    public Object getItem(int position) {
        return list_itemArrayList.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if(convertView == null){
            convertView = LayoutInflater.from(context).inflate(R.layout.item,null);

            capturedImageView = (ImageView) convertView.findViewById(R.id.captured_imageview);
            title =  (TextView) convertView.findViewById(R.id.title_textview);
        }

        title.setText(list_itemArrayList.get(position).getTitle());
        byte[] bytes = list_itemArrayList.get(position).getCapturedImage();
        capturedImageView.setImageBitmap(BitmapFactory.decodeByteArray(bytes, 0, bytes.length));

        return convertView;
    }
}

