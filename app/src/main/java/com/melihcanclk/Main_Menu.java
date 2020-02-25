package com.melihcanclk;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

public class Main_Menu extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main__menu);

        final Spinner spinner1 = (Spinner) findViewById(R.id.spinner1);
        final Spinner spinner2 = (Spinner) findViewById(R.id.spinner2);

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(Main_Menu.this,
                android.R.layout.simple_list_item_1,
                getResources().getStringArray(R.array.numbers));

        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner1.setAdapter(adapter);
        spinner2.setAdapter(adapter);

        Button button = (Button) findViewById(R.id.button_start);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Everytime user click this button, new second activity will be launched
                int row = Integer.parseInt(spinner1.getSelectedItem().toString());
                int column = Integer.parseInt(spinner2.getSelectedItem().toString());

                //pass mainActivity values of spinners
                Intent intent = MainActivity.makeIntent(Main_Menu.this,column,row);
                startActivity(intent);
            }
        });
    }
}
