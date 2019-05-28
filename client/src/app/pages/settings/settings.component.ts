import { ApiService } from './../../services/api.service';
import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
})
export class SettingsComponent implements OnInit {

  apiKey = '';
  endpoint = '';

  constructor(private api: ApiService, private snackBar: MatSnackBar) { }

  ngOnInit() {
    this.api.getSetting().subscribe(
      result => {
        this.apiKey = result.apiKey;
        this.endpoint = result.endpoint;
      },
      error => {
        console.log(error);
      }
    );
  }

  submit() {
    this.api.createSetting({apiKey: this.apiKey, endpoint: this.endpoint}).subscribe(
      result => {
        console.log('success');
        if (result.apiKey !== '') {
          this.snackBar.open('登録しました', '閉じる', {
            duration: 5000,
          });
        } else {
          this.snackBar.open('登録に失敗しました', '閉じる', {
            duration: 5000,
          });
        }

      },
      error => {
        console.log(error);

      }
    );
  }

}
