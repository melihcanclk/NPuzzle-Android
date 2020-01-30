package com.example.npuzzle;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class Main_Menu extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main__menu);

        Button button = (Button) findViewById(R.id.button_start);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //Everytime user click this button, new second activity will be launched
                Intent intent = MainActivity.makeIntent(Main_Menu.this);
                startActivity(intent);
            }
        });
    }
}
