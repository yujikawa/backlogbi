import { Component, OnInit, Input, ViewChild, AfterViewInit, ElementRef } from '@angular/core';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent implements OnInit, AfterViewInit {
  @Input() canvasWidth = 100;
  @Input() canvasHeight = 100;
  @Input() data;

  @ViewChild('chart')
  ref: ElementRef;

  context: CanvasRenderingContext2D;
  chart: Chart;

  constructor() { }

  ngOnInit() {
  }

  ngAfterViewInit() {
    // canvasを取得
    this.context = this.ref.nativeElement.getContext('2d');
    // チャートの作成
    this.chart = new Chart(this.context, this.data);
  }
}
