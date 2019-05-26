import { Observable } from 'rxjs';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource } from '@angular/material';

import { IssueStats } from './../../models/issue_stats';
import { Project } from './../../models/project';
import { Count } from './../../models/count';
import { UserStats } from './../../models/member_stats';
import { ApiService } from './../../services/api.service';
import { range } from '../../utils/caluc';
import * as moment from 'moment';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  displayedColumns: string[] = ['user', 'category', 'status', 'actualAvgTime'];
  dataSource: MatTableDataSource<UserStats>;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  issues: IssueStats;
  $issues: Observable<IssueStats>;
  selectedProjectId: number;
  projects: Array<Project> = [];
  selectedMonth = moment().format('YYYY-MM');

  COLOR_BG: Array<string> = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(150, 200, 200, 1)'
  ];

  COLOR_BORFER: Array<string> = [
    'rgba(255,99,132,1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(150, 200, 200, 1)'
  ];

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.api.getProjects().subscribe(
      result => {
        this.projects = result;
        this.selectedProjectId = this.projects[0].id;
        this.reload();
      },
      error => { }
    );

  }

  reload() {
    this.$issues = this.api.getStatsIssues(this.selectedMonth, this.selectedProjectId);
    this.api.getStatsMembers(this.selectedMonth, this.selectedProjectId).subscribe(
      resultMem => {
        this.dataSource = new MatTableDataSource<UserStats>(resultMem.users);
        this.dataSource.paginator = this.paginator;
      },
      error => {
        console.error(error);
      }
    );
  }

  makePieDataMonthlyByUser(issues: UserStats): any {
    const data = {
      type: 'pie',
      data: {
        labels: issues.byCategories.map((e, index, array) => {
          return e.name;
        }),
        datasets: [{
          // label: '# of Votes',
          data: issues.byCategories.map((e, index, array) => {
            return e.count;
          }),
          backgroundColor: this.COLOR_BG,
          borderColor: this.COLOR_BORFER,
          borderWidth: 1
        }]
      },      // データをプロパティとして渡す
      options: {
        // legend: false,
      } // オプションをプロパティとして渡す
    };
    return data;
  }

  makeBarDataMonthlyByUser(issues: UserStats): any {
    const data = {
      type: 'horizontalBar',     // とりあえず doughnutチャートを表示
      data: {
        // labels: range(parseInt(startDate, 10), parseInt(endDate, 10)),
        datasets: issues.byStatus.map((e, index, array) => {
          return {
            data: [(e.count as Array<number>).reduce((acc, currentVal) => {
              return acc + currentVal;
            }, 0)],
            label: e.name,
            backgroundColor: this.COLOR_BG[e.id % this.COLOR_BG.length]
          };
        })
      },      // データをプロパティとして渡す
      options: {
        scales: {
          xAxes: [{
            stacked: true,
            ticks: {
              stepSize: 1
            },
          }],
          yAxes: [{
            stacked: true,

          }]
        }
      } // オプションをプロパティとして渡す
    };
    return data;
  }

  makePieDataMonthly(issues: IssueStats): any {
    const data = {
      type: 'pie',
      data: {
        labels: issues.byCategories.map((e, index, array) => {
          return e.name;
        }),
        datasets: [{
          // label: '# of Votes',
          data: issues.byCategories.map((e, index, array) => {
            return e.count;
          }),
          backgroundColor: this.COLOR_BG,
          borderColor: this.COLOR_BORFER,
          borderWidth: 1
        }]
      },      // データをプロパティとして渡す
      options: {
        // legend: false,
      } // オプションをプロパティとして渡す
    };
    return data;
  }

  makeBarDataMonthly(issues: IssueStats): any {
    const startDate: string = issues.statsInfo.dueDateSince.split('-')[2];
    const endDate: string = issues.statsInfo.dueDateUntil.split('-')[2];

    const data = {
      type: 'bar',     // とりあえず doughnutチャートを表示
      data: {
        labels: range(parseInt(startDate, 10), parseInt(endDate, 10)),
        datasets: issues.byStatus.map((e, index, array) => {
          return {
            data: e.count,
            label: e.name,
            backgroundColor: this.COLOR_BG[e.id % this.COLOR_BG.length]
          };
        })
      },      // データをプロパティとして渡す
      options: {
        scales: {
          xAxes: [{
            stacked: true
          }],
          yAxes: [{
            stacked: true,
            ticks: {
              stepSize: 1
            },
          }]
        }
      } // オプションをプロパティとして渡す
    };
    return data;
  }




}
