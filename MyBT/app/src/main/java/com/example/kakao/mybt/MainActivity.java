package com.example.kakao.mybt;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.SystemClock;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.lang.reflect.Method;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Set;
import java.util.UUID;






public class MainActivity extends AppCompatActivity {



    // GUI Components
    private TextView mBluetoothStatus;
    private TextView mReadBuffer;
    private TextView mOn;
    private TextView mOff;
    private TextView mListPairedDevices;
    private TextView mDiscover;
    private TextView mExit;
    private TextView mText;

    private Button   mCapture;
    private Button   mShowFeed;
    private ListView mDevicesListView;
    private CheckBox mCheckboxCam;
    private CheckBox mCheckboxTimelapse;
    private SeekBar  mSeekBarCameraPeriod;

    private ImageView mImageView;

    // Image view settings
    private itemHolder m_itemHolder;
    private MyImageAdapter myImageAdapter;

    // BT settings
    private BluetoothAdapter mBTAdapter;
    private ArrayAdapter<String> mBTArrayAdapter;

    private Set<BluetoothDevice> mPairedDevices;



    private final String TAG = MainActivity.class.getSimpleName();

    private static Handler mHandler; // Our main handler that will receive callback notifications
    private ConnectedThread mConnectedThread; // bluetooth background worker thread to send and receive data
    private BluetoothSocket mBTSocket = null; // bi-directional client-to-client data path

    private static final UUID BTMODULEUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"); // "random" unique identifier

    // #defines for identifying shared types between calling functions
    private final static int REQUEST_ENABLE_BT = 1; // used to identify adding bluetooth names
    private final static int MESSAGE_READ = 2; // used in bluetooth handler to identify message update
    private final static int CONNECTING_STATUS = 3; // used in bluetooth handler to identify message status

    private final static int BT_CONNECTION_SUCCEED = 1; // used to check whether BT connection has been completed between phone and pi
    private final static int BT_CONNECTION_FAILED = 0;

    private final static int IMAGE_SENT_SUCCEED = 1;// used to check whether image sent from pi has succeeded
    private final static int IF_COUNT_MSG = 0;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        java.lang.System.setProperty("java.net.preferIPv4Stack", "true");
        java.lang.System.setProperty("java.net.preferIPv6Addresses", "false");

        /*****************************
         *  Variable Settinigs       *
         ****************************/

        mText = (TextView) findViewById(R.id.text);

        mBluetoothStatus = (TextView) findViewById(R.id.bluetoothStatus);
        mReadBuffer = (TextView) findViewById(R.id.readBuffer);
        mOn = (TextView) findViewById(R.id.on);
        mOff = (TextView) findViewById(R.id.off);
        mListPairedDevices = (TextView) findViewById(R.id.PairedBtn);
        mDiscover = (TextView) findViewById(R.id.discoverBtn);
        mExit = (TextView) findViewById(R.id.exit);
        mCapture = (Button) findViewById(R.id.captureBtn);
        mShowFeed = (Button) findViewById(R.id.showFeed);
        mCheckboxCam = (CheckBox) findViewById(R.id.checkboxCam);
        mCheckboxTimelapse = (CheckBox) findViewById(R.id.checkboxTimelapse);
        mSeekBarCameraPeriod = (SeekBar) findViewById(R.id.seekBarCameraPeriod);

        //checkbox default setting
        mCheckboxTimelapse.setEnabled(false);
        mCheckboxCam.setEnabled(false);

        mCheckboxTimelapse.setChecked(false);
        mCheckboxCam.setChecked(false);
        mSeekBarCameraPeriod.setEnabled(false);

        mImageView = (ImageView) findViewById(R.id.photo_imageview);

        //BT setting
        mBTArrayAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1);
        mBTAdapter = BluetoothAdapter.getDefaultAdapter(); // get a handle on the bluetooth radio

        mDevicesListView = (ListView) findViewById(R.id.devicesListView);
        mDevicesListView.setAdapter(mBTArrayAdapter); // assign model to view
        mDevicesListView.setOnItemClickListener(mDeviceClickListener);

        //Image setting

        m_itemHolder = itemHolder.getInstance();
        myImageAdapter = new MyImageAdapter(this, m_itemHolder.getList_item());

        // Ask for location permission if not already allowed
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED)
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_COARSE_LOCATION}, 1);


        mHandler = new Handler() {
            public void handleMessage(android.os.Message msg) {
                if (msg.what == MESSAGE_READ) {
                    if(msg.arg1 == IMAGE_SENT_SUCCEED) {
                        //byte[] bytes = ((list_item)msg.obj).getCapturedImage();
                        byte[] bytes = (byte[])msg.obj;
                        Bitmap bmp = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                        mImageView.setImageBitmap(bmp);
                        //mText.setText(String.valueOf(msg.arg2));
                        //mlist_item.add((list_item)msg.obj);

                    }
                    if (msg.arg1 == IF_COUNT_MSG)
                    {
                        String readMessage = String.valueOf(msg.arg2);
                        mReadBuffer.setText(readMessage);
                    }
                }

                if (msg.what == CONNECTING_STATUS) {
                    if (msg.arg1 == BT_CONNECTION_SUCCEED) {
                        mBluetoothStatus.setText("Connected to Device: " + (String) (msg.obj));
                        //checkbox enable after BT connection
                        mCheckboxTimelapse.setEnabled(true);
                        mCheckboxCam.setEnabled(true);
                    }
                    else {
                        mText.setText(String.valueOf(msg.arg2));
                        mBluetoothStatus.setText("Connection Failed");
                    }
                }
            }
        };


        /*****************************
         *  code starts from here    *
         ****************************/

        mShowFeed.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                //if (mConnectedThread != null) { //First check to make sure thread created
                //    // send msg to pi to call images
                //    mConnectedThread.writeInJson(Constants.LD_IMAGE, Constants.NOTHING);
                //}
                // create intent to go to feed
                if(mConnectedThread != null){
                    mConnectedThread.writeInJson(Constants.LD_IMAGE, Constants.NOTHING);
                    Log.d(TAG, "message send finish");
                    mConnectedThread.readImages();
                }

                Intent feedIntent = new Intent(getApplicationContext(), feedActivity.class); // view.getContext() indicates MainActivity, this

                startActivity(feedIntent);

            }
        });

        if (mBTArrayAdapter == null) {
            // Device does not support Bluetooth
            mBluetoothStatus.setText("Status: Bluetooth not found");
            Toast.makeText(getApplicationContext(), "Bluetooth device not found!", Toast.LENGTH_SHORT).show();
        } else {

            mOn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    bluetoothOn(v);
                }
            });

            mOff.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    bluetoothOff(v);
                }
            });

            mDiscover.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    discover(v);
                }
            });

            mListPairedDevices.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    listPairedDevices(v);
                }
            });


            mExit.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (mConnectedThread != null) { //First check to make sure thread created
                        mConnectedThread.writeInJson(Constants.BT_OFF, Constants.NOTHING);

                        mConnectedThread.cancel();

                        try {
                            mBTSocket.close();
                            mBluetoothStatus.setText("bluetooth disconnected");
                            if(mCheckboxCam.isChecked())
                                mCheckboxCam.setChecked(false);// checkbox off
                            if(mCheckboxTimelapse.isChecked())
                                mCheckboxTimelapse.setChecked(false);// checkbox off

                        } catch(IOException e){
                            Log.e(TAG, "closing bluetooth failed!", e);
                            Toast.makeText(getApplicationContext(), "closing bluetooth failed!", Toast.LENGTH_SHORT).show();
                        }
                    }
                }
            });



            mCapture.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v){
                    if(mConnectedThread != null) //First check to make sure thread created
                        mConnectedThread.writeInJson(Constants.CAM_CAPTURE, Constants.NOTHING); //capture
                }
            });

            mCheckboxCam.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mConnectedThread != null){ //First check to make sure thread created
                        if (mCheckboxCam.isChecked()) {
                            mConnectedThread.writeInJson(Constants.CAM_ON, Constants.NOTHING); //start capturing
                            mSeekBarCameraPeriod.setEnabled(true);
                        }
                        else {
                            mConnectedThread.writeInJson(Constants.CAM_OFF, Constants.NOTHING); //quit from capturing mode
                            mSeekBarCameraPeriod.setEnabled(false);
                        }
                    }
                }
            });

            mCheckboxTimelapse.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mConnectedThread != null){ //First check to make sure thread created
                        if (mCheckboxTimelapse.isChecked()){
                            mConnectedThread.writeInJson(Constants.TIMELAPSE_ON,Constants.NOTHING); //start capturing
                            //disable clicking mCheckboxCam
                            mCheckboxCam.setEnabled(false);
                            mSeekBarCameraPeriod.setEnabled(false);

                        }
                        else{
                            mConnectedThread.writeInJson(Constants.TIMELAPSE_OFF,Constants.NOTHING); //quit from capturing mode
                            //enable clicking mCheckboxCam
                            mCheckboxCam.setEnabled(true);
                            if(mCheckboxCam.isChecked()){
                                mSeekBarCameraPeriod.setEnabled(true);
                            }
                            else{
                                mSeekBarCameraPeriod.setEnabled(false);
                            }
                        }

                    }
                }
            });

            mSeekBarCameraPeriod.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
                private int camPeriod;
                @Override
                public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                     camPeriod = i;
                }
                @Override
                public void onStartTrackingTouch(SeekBar seekBar) {//do nothing
                }

                @Override
                public void onStopTrackingTouch(SeekBar seekBar) {
                    if (mConnectedThread != null) { //First check to make sure thread created
                        mConnectedThread.writeInJson(Constants.CAM_PERIOD, String.valueOf(camPeriod)); //start capturing
                    }
                }
            });



        }
    }



    private void bluetoothOn(View view) {
        if (!mBTAdapter.isEnabled()) {
            Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            mBluetoothStatus.setText("Bluetooth enabled");
            Toast.makeText(getApplicationContext(), "Bluetooth turned on", Toast.LENGTH_SHORT).show();

        } else {
            Toast.makeText(getApplicationContext(), "Bluetooth is already on", Toast.LENGTH_SHORT).show();
        }
    }

    // Enter here after user selects "yes" or "no" to enabling radio
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent Data) {
        // Check which request we're responding to
        if (requestCode == REQUEST_ENABLE_BT) {
            // Make sure the request was successful
            if (resultCode == RESULT_OK) {
                // The user picked a contact.
                // The Intent's data Uri identifies which contact was selected.
                mBluetoothStatus.setText("Enabled");
            } else
                mBluetoothStatus.setText("Disabled");
        }
    }

    private void bluetoothOff(View view) {
        mBTAdapter.disable(); // turn off
        mBluetoothStatus.setText("Bluetooth disabled");
        Toast.makeText(getApplicationContext(), "Bluetooth turned Off", Toast.LENGTH_SHORT).show();
    }

    private void discover(View view) {
        // Check if the device is already discovering
        if (mBTAdapter.isDiscovering()) {
            mBTAdapter.cancelDiscovery();
            Toast.makeText(getApplicationContext(), "Discovery stopped", Toast.LENGTH_SHORT).show();
        } else {
            if (mBTAdapter.isEnabled()) {
                mBTArrayAdapter.clear(); // clear items
                mBTAdapter.startDiscovery();
                Toast.makeText(getApplicationContext(), "Discovery started", Toast.LENGTH_SHORT).show();
                registerReceiver(blReceiver, new IntentFilter(BluetoothDevice.ACTION_FOUND));
            } else {
                Toast.makeText(getApplicationContext(), "Bluetooth not on", Toast.LENGTH_SHORT).show();
            }
        }
    }

    final BroadcastReceiver blReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                // add the name to the list
                mBTArrayAdapter.add(device.getName() + "\n" + device.getAddress());
                mBTArrayAdapter.notifyDataSetChanged();
            }
        }
    };

    private void listPairedDevices(View view) {
        mPairedDevices = mBTAdapter.getBondedDevices();
        if(mPairedDevices == null){
            discover(view);
        }

        if (mBTAdapter.isEnabled()) {
            // put it's one to the adapter
            for (BluetoothDevice device : mPairedDevices)
                mBTArrayAdapter.add(device.getName() + "\n" + device.getAddress());

            Toast.makeText(getApplicationContext(), "Show Paired Devices", Toast.LENGTH_SHORT).show();
        } else
            Toast.makeText(getApplicationContext(), "Bluetooth not on", Toast.LENGTH_SHORT).show();
        mBTAdapter.cancelDiscovery();
        }

        private AdapterView.OnItemClickListener mDeviceClickListener = new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> av, View v, int arg2, long arg3) {

                if (!mBTAdapter.isEnabled()) {
                    Toast.makeText(getBaseContext(), "Bluetooth not on", Toast.LENGTH_SHORT).show();
                    return;
                }

            mBluetoothStatus.setText("Connecting...");
            // Get the device MAC address, which is the last 17 chars in the View
            String info = ((TextView) v).getText().toString();
            final String address = info.substring(info.length() - 17);
            final String name = info.substring(0, info.length() - 17);

            // Spawn a new thread to avoid blocking the GUI one
            ConnectThread connectTh = new ConnectThread(address, name);
            connectTh.start();
        }
    };

    private BluetoothSocket createBluetoothSocket(BluetoothDevice device) throws IOException {
        try {
            final Method m = device.getClass().getMethod("createInsecureRfcommSocketToServiceRecord", UUID.class);
            return (BluetoothSocket) m.invoke(device, BTMODULEUUID);
        } catch (Exception e) {
            Log.e(TAG, "Could not create Insecure RFComm Connection", e);
        }
        return device.createRfcommSocketToServiceRecord(BTMODULEUUID);
    }

    private class ConnectThread extends Thread {
            private String address;
            private String name;

        public ConnectThread(String address, String name) {
            this.address = address;
            this.name = name;
        }

        public void run() {
            boolean BTsocketCreated = false;
            boolean BTsocketConnected = false;

            BluetoothDevice device = mBTAdapter.getRemoteDevice(address);
            try {
                mBTSocket = createBluetoothSocket(device);
                BTsocketCreated = true;
            } catch (IOException e) {
                Log.e(TAG, "Socket creation failed", e);
                Toast.makeText(getBaseContext(), "Socket creation failed", Toast.LENGTH_SHORT).show();
            }
            // Establish the Bluetooth socket connection.
            //stop discovering before connection
            //mBTAdapter.cancelDiscovery();

            try {
                mBTSocket.connect();
                BTsocketConnected = true;
            } catch (IOException e) {
                try {
                    mBTSocket.close();
                    mHandler.obtainMessage(CONNECTING_STATUS, BT_CONNECTION_FAILED, -1)
                            .sendToTarget();
                    Log.d(TAG, "---------------------"+BTsocketConnected + " " + BTsocketCreated + "---------");
                } catch (IOException e2) {
                    Log.e(TAG, "Socket creation failed", e);
                    Toast.makeText(getBaseContext(), "Socket creation failed", Toast.LENGTH_SHORT).show();
                }
            }



            if (BTsocketCreated && BTsocketConnected) {
                // create connected thread
                mConnectedThread = new ConnectedThread(mBTSocket);
                mConnectedThread.start();
                Log.d(TAG, "0000000000000000000000000--"+BTsocketConnected + " " + BTsocketCreated + "---------");
                mHandler.obtainMessage(CONNECTING_STATUS, BT_CONNECTION_SUCCEED, -1, name)
                        .sendToTarget();
            }
        }

        public void cancel(){
            //do nothing
            //UI message
            //
            try{
                mBTSocket.close();
            } catch (IOException e){}
        }

    }

    private class ConnectedThread extends Thread {
        private final BluetoothSocket mmSocket;
        private final InputStream mmInStream;
        private final OutputStream mmOutStream;
        private boolean is_running = false;

        public ConnectedThread(BluetoothSocket socket) {
            mmSocket = socket;
            InputStream tmpIn = null;
            OutputStream tmpOut = null;


            // Get the input and output streams, using temp objects because
            // member streams are final
            try {
                tmpIn = socket.getInputStream();
                tmpOut = socket.getOutputStream();
            } catch (IOException e) {

            }

            mmInStream = tmpIn;
            mmOutStream = tmpOut;
            is_running = true;
        }

        public void run() {
            while(this.is_running){
                try{
                    Thread.sleep(1000);
                    Log.d(TAG, "CONNECTED THREAD RUNNING...");
                }
                catch(InterruptedException e){
                    Log.e(TAG, "thread sleep failed", e);
                }

            }
            Log.d(TAG, "CONNECED THREAD TERMINATED...");

        }

        /* Call this from the main activity to send data to the remote device */
        public void writeInJson(String msg, String value) {
            String jsonStr = String.format("{\"msg\" : \"%s\", \"value\" : \"%s\"}", msg, value);

            byte[] bytes = jsonStr.getBytes();           //converts entered String into bytes
            try {
                mmOutStream.write(bytes);
            } catch (IOException e) {
                Log.e(TAG, "stream write failed", e);
            }
        }

        public void readImages() {
            // if 몇번 도는지 체크
            byte[] byte_titleLength = new byte[4];
            byte[] byte_imageLength = new byte[4];
            byte[] byte_tank = new byte[200000];

            int imageLength=0;
            int titleLength = 0;

            String s_img = "";

            int imageIndex=0;

            int count = 0;

            while(true){
                s_img = "";
                imageIndex = 0;
                imageLength = 0;
                titleLength = 0;
                count +=1;


                // Keep listening to the InputStream until an exception occurs
                try {
                    // Read title from the InputStream
                    mmInStream.read(byte_titleLength,0,4);


                    titleLength = ByteBuffer.wrap(byte_titleLength).getInt();
                    if(titleLength == Constants.TERMINATE_CODE){// message for termination
                        Log.d(TAG, "got termination codon");
                        break;
                    }

                    Log.d(TAG, "title length : "+String.valueOf(titleLength));

                    byte[] titleBuf = new byte[titleLength];
                    mmInStream.read(titleBuf, 0, titleLength);

                    String s_title = new String(titleBuf);

                    // Read Image from the InputStream
                    mmInStream.read(byte_imageLength,0,4);
                    imageLength = ByteBuffer.wrap(byte_imageLength).getInt();

                    Log.d(TAG, "image length : "+String.valueOf(imageLength));


                    while(imageIndex < imageLength){
                        byte[] curBuf = new byte[1];
                        mmInStream.read(curBuf);
                        byte_tank[imageIndex] = curBuf[0];
                        imageIndex += 1;
                    }

                    byte[] b_img = Arrays.copyOfRange(byte_tank, 0, imageIndex);


                    Log.d(TAG, "title name : "+ s_title);
                    Log.d(TAG, "image size : "+ String.valueOf(b_img.length));



                    item newImgItem = new item(s_title, b_img);

                    m_itemHolder = itemHolder.getInstance();
                    m_itemHolder.append_item(newImgItem);


                    Log.d(TAG, "final image size : "+String.valueOf(imageIndex));

                    mHandler.obtainMessage(MESSAGE_READ, IMAGE_SENT_SUCCEED, imageIndex, b_img).sendToTarget();


                } catch (IOException e) {
                    mHandler.obtainMessage(MESSAGE_READ, IF_COUNT_MSG, 3,1).sendToTarget();
                    e.printStackTrace();
                    break;
                }
            }
            Log.d(TAG, "Reading image done! ");
        }



        /* Call this from the main activity to shutdown the connection */
        public void cancel() {
            is_running = false;
            try {
                mmSocket.close();
            } catch (IOException e) {
                Log.e(TAG, "socket closing failed", e);
            }
        }
    }



}
