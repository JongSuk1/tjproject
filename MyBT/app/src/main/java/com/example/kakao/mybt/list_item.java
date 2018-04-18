package com.example.kakao.mybt;

import android.graphics.Bitmap;
import android.os.Parcel;
import android.os.Parcelable;

/**
 * Created by kakao on 2018. 4. 13..
 */

public class list_item implements Parcelable {
    private String title;
    private byte[] capturedImageByte=null;

    public list_item(String title, byte[] capturedImage) {
        this.title = title;
        this.capturedImageByte = capturedImage;
    }


    protected list_item(Parcel in) {
        title = in.readString();
        capturedImageByte = in.createByteArray();
    }

    public static final Creator<list_item> CREATOR = new Creator<list_item>() {
        @Override
        public list_item createFromParcel(Parcel in) {
            return new list_item(in);
        }

        @Override
        public list_item[] newArray(int size) {
            return new list_item[size];
        }
    };

    public String getTitle(){
        return this.title;
    }

    public byte[] getCapturedImage(){
        return this.capturedImageByte;
    }


    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel parcel, int i) {

        parcel.writeString(title);
        parcel.writeByteArray(capturedImageByte);
    }
}
