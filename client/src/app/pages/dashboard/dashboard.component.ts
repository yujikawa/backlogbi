import { Component, OnInit, ViewChild, AfterViewInit, ElementRef } from '@angular/core';
import { MatPaginator, MatTableDataSource } from '@angular/material';
import { Chart, ChartData, ChartOptions } from 'chart.js';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {
  displayedColumns: string[] = ['user', 'category', 'doneTask', 'allTasks', 'diff', 'wiki', 'star', 'partner'];
  dataSource = new MatTableDataSource<PeriodicElement>(ELEMENT_DATA);
  @ViewChild(MatPaginator) paginator: MatPaginator;

  @ViewChild('category')
  ref1: ElementRef;

  @ViewChild('task')
  ref2: ElementRef;

  context1: CanvasRenderingContext2D;
  context2: CanvasRenderingContext2D;

  chart1: Chart;
  chart2: Chart;

  constructor() { }

  ngOnInit() {
    this.dataSource.paginator = this.paginator;


  }

  ngAfterViewInit() {
    // canvasを取得
    this.context1 = this.ref1.nativeElement.getContext('2d');
    this.context2 = this.ref2.nativeElement.getContext('2d');

    // チャートの作成
    this.chart1 = new Chart(this.context1, {
      type: 'pie',     // とりあえず doughnutチャートを表示
      data: {
        labels: ['開発', '運用', '障害', 'その他'],
        datasets: [{
          label: '# of Votes',
          data: [12, 19, 3, 5],
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            // 'rgba(75, 192, 192, 0.2)',
            // 'rgba(153, 102, 255, 0.2)',
            'rgba(150, 200, 200, 0.2)'
          ],
          borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            // 'rgba(75, 192, 192, 1)',
            // 'rgba(153, 102, 255, 1)',
            'rgba(150, 200, 200, 1)'
          ],
          borderWidth: 1
        }]
      },      // データをプロパティとして渡す
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      } // オプションをプロパティとして渡す
    });

    // チャートの作成
    this.chart2 = new Chart(this.context2, {
      type: 'bar',     // とりあえず doughnutチャートを表示
      data: {
        labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
        datasets: [{
          data: [4, 5, 9, 14, 15, 24, 30, 10, 4, 5, 2, 10],
          label: '完了',
          backgroundColor: 'rgba(168, 207, 240, 1)'
        },
        {
          data: [0.4, 0.5, 0.9, 1.4, 1.5, 2, 4, 3.0, 3, 4, 5, 2, 1],
          label: '未完了',
          backgroundColor: 'rgba(252, 165, 175, 1)'
        }]
      },      // データをプロパティとして渡す
      options: {
        scales: {
          xAxes: [{
            stacked: true
          }],
          yAxes: [{
            stacked: true
          }]
        }
      } // オプションをプロパティとして渡す
    });

  }

}
class User {
  name: string;
  icon: string;
}
export interface PeriodicElement {
  user: User;
  category: Array<number>;
  doneTask: number;
  allTasks: number;
  diff: string;
  wiki: number;
  star: number;
  partner: User;
}

const ELEMENT_DATA: PeriodicElement[] = [
  {
    user: { name: 'kawakami', icon: 'https://www.karabiner.tech/asset/images/common/member_lee.jpg' },
    category: [20, 10, 20, 20],
    doneTask: 40,
    allTasks: 50,
    diff: '-2~+3',
    wiki: 10,
    star: 10,
    partner: { name: 'kotaro', icon: 'https://www.karabiner.tech/asset/images/common/member_kotaro.jpg' },
  },
  {
    user: { name: 'kawakami', icon: 'https://www.karabiner.tech/asset/images/common/member_lee.jpg' },
    category: [20, 10, 20, 20],
    doneTask: 40,
    allTasks: 50,
    diff: '-2~+3',
    wiki: 10,
    star: 10,
    partner: { name: 'kotaro', icon: 'https://www.karabiner.tech/asset/images/common/member_kotaro.jpg' },
  },
  {
    user: { name: 'kawakami', icon: 'https://www.karabiner.tech/asset/images/common/member_lee.jpg' },
    category: [20, 10, 20, 20],
    doneTask: 40,
    allTasks: 50,
    diff: '-2~+3',
    wiki: 10,
    star: 10,
    partner: { name: 'kotaro', icon: 'https://www.karabiner.tech/asset/images/common/member_kotaro.jpg' },
  },
];
