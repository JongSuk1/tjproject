package com.example.kakao.mybt;

import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothServerSocket;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;


class SharedArea{
    BluetoothAdapter btAdapter;
    boolean isReady; //check if shared data has been used
};

class AcceptThread extends Thread {
    private final BluetoothServerSocket mmServerSocket;
    BluetoothAdapter myBluetoothAdapter;

    public AcceptThread() {
        // Use a temporary object that is later assigned to mmServerSocket,
        // because mmServerSocket is final
        BluetoothServerSocket tmp = null;
        UUID MY_UUID = UUID.fromString(myBluetoothAdapter.getAddress());
        String NAME = myBluetoothAdapter.getName();
        try {
            // MY_UUID is the app's UUID string, also used by the client code
            tmp = myBluetoothAdapter.listenUsingRfcommWithServiceRecord(NAME, MY_UUID);
        } catch (IOException e) { }
        mmServerSocket = tmp;
    }

    public void run() {
        BluetoothSocket socket = null;
        // Keep listening until exception occurs or a socket is returned
        while (true) {
            try {
                socket = mmServerSocket.accept();
            } catch (IOException e) {
                break;
            }
            // If a connection was accepted
            if (socket != null) {
                // Do work to manage the connection (in a separate thread)
                manageConnectedSocket(socket);
                try {
                    mmServerSocket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                break;
            }
        }
    }

    private void manageConnectedSocket(BluetoothSocket socket) {
        //do something


    }

    /** Will cancel the listening socket, and cause the thread to finish */
    public void cancel() {
        try {
            mmServerSocket.close();
        } catch (IOException e) { }
    }
}

public class MainActivity extends AppCompatActivity implements OnItemClickListener {

    TextView onBtn;
    TextView offBtn;
    TextView listBtn;
    TextView findBtn,dk;
    TextView text;
    AcceptThread thread;
    ArrayAdapter<String> mArrayAdapter;
    BluetoothAdapter myBluetoothAdapter;
    BroadcastReceiver mReceiver;
    ArrayList<BluetoothDevice> mDeviceList = new ArrayList<BluetoothDevice>();
    ArrayList<String> strDeviceList = new ArrayList<String>();

    int REQUEST_ENABLE_BT = 1;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        text = (TextView) findViewById(R.id.text);
        onBtn = (TextView)findViewById(R.id.turnOn);
        offBtn = (TextView)findViewById(R.id.turnOff);
        dk = (TextView) findViewById(R.id.mk);
        listBtn = (TextView)findViewById(R.id.paired);
        findBtn = (TextView)findViewById(R.id.search);
        final ListView myListView = (ListView)findViewById(R.id.listView1);


        strDeviceList.add("initial one.");
        mArrayAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, strDeviceList);


        myBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();



        if (myBluetoothAdapter == null) {
            showUnsupported();
        }
        else {
            //find the bluetooth enable or disable
            if (myBluetoothAdapter.isEnabled()) {
                showEnabled();
            } else {
                showDisabled();
            }
        }

        dk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                makeDiscoverable();
            }
        });

        listBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v){
                myListView.setAdapter(mArrayAdapter);
            }
        });



        findBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                // paired device check; if exists, add to listview

                    /*
                    Set<BluetoothDevice> pairedDevices = myBluetoothAdapter.getBondedDevices();
                    text.setText("hi");
                    if(pairedDevices.size() > 0){
                        //Loop through paired devices
                        for (BluetoothDevice device : pairedDevices){
                            // Add the name and address to an array adapter to show in a listview
                            mArrayAdapter.add(device.getName() + "\n" + device.getAddress());
                            //strDeviceList.add(device.getName() + "\n" + device.getAddress());
                        }
                    }
                    else{*/
                // start finding device
                //if (!myBluetoothAdapter.isDiscovering()){
                    // BTArrayAdapter.clear();
                    // Create a BroadcastReceiver for ACTION_FOUND

                    mReceiver = new BroadcastReceiver() {
                        public void onReceive(Context context, Intent intent) {
                            String action = intent.getAction();
                            // When discovery finds a device
                            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                                // Get the BluetoothDevice object from the Intent
                                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                                strDeviceList.add(device.getName() + "\n" + device.getAddress());
                                text.setText(device.getName() + "\n" + device.getAddress());
                                // Add the name and address to an array adapter to show in a ListView
                                //mArrayAdapter.add(device.getName() + "\n" + device.getAddress());
                            }
                        }
                    };
                    IntentFilter filter = new IntentFilter();
                    filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_STARTED);
                    filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
                    filter.addAction(BluetoothDevice.ACTION_FOUND);
                    registerReceiver(mReceiver, filter);

                    if(myBluetoothAdapter.isDiscovering()){
                        myBluetoothAdapter.cancelDiscovery();
                    }
                    myBluetoothAdapter.startDiscovery();

                //}
            }
        });



        onBtn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent turnOnIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                    startActivityForResult(turnOnIntent, REQUEST_ENABLE_BT);
               }
        });

        offBtn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    myBluetoothAdapter.disable();
                    showDisabled();
                }
        });
    }




    @Override
    public void onPause() {
        if (myBluetoothAdapter != null) {
            if (myBluetoothAdapter.isDiscovering()) {
                myBluetoothAdapter.cancelDiscovery();
            }
        }

        super.onPause();
    }

    @Override
    public void onDestroy() {
        unregisterReceiver(mReceiver);

        super.onDestroy();
    }

    private void showEnabled() {
        text.setText("Bluetooth is On");
        text.setTextColor(Color.BLUE);
        offBtn.setEnabled(true);
        onBtn.setEnabled(false);

    }

    private void showDisabled() {
        text.setText("Bluetooth is Off");
        text.setTextColor(Color.RED);
        offBtn.setEnabled(false);
        onBtn.setEnabled(true);

    }

    private void showUnsupported() {
        text.setText("Bluetooth is unsupported by this device");
    }

    private void makeDiscoverable() {
        Intent discoverableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
        discoverableIntent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300);
        startActivity(discoverableIntent);

    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
        text.setText(i);
        AcceptThread th;



    }
}
