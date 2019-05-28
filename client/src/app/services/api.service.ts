import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment as env } from '../../environments/environment';
import { IssueStats } from '../models/issue_stats';
import { MemberStats } from '../models/member_stats';
import { Setting } from './../models/setting';
import { Project } from './../models/project';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  getSetting(): Observable<Setting> {
    return this.http.get<Setting>(`${env.apiBaseUrl}/settings`,
      {
        headers: new HttpHeaders(
          { 'Content-Type': 'application/json' }
        )
      }
    );
  }

  createSetting(data): Observable<Setting> {
    return this.http.post<Setting>(`${env.apiBaseUrl}/settings`, JSON.stringify(data),
      {
        headers: new HttpHeaders(
          { 'Content-Type': 'application/json' }
        )
      }
    );
  }

  getProjects(): Observable<Array<Project>> {
    return this.http.get<Array<Project>>(`${env.apiBaseUrl}/projects`,
      {
        headers: new HttpHeaders(
          { 'Content-Type': 'application/json' }
        )
      }
    );
  }

  getStatsIssues(yyyymm: string, projectId: number): Observable<IssueStats> {
    return this.http.get<IssueStats>(`${env.apiBaseUrl}/stats/issues?yyyymm=${yyyymm}&projectId=${projectId}`,
      {
        headers: new HttpHeaders(
          { 'Content-Type': 'application/json' }
        )
      }
    );
  }

  getStatsMembers(yyyymm: string, projectId: number): Observable<MemberStats> {
    return this.http.get<MemberStats>(`${env.apiBaseUrl}/stats/members?yyyymm=${yyyymm}&projectId=${projectId}`,
      {
        headers: new HttpHeaders(
          { 'Content-Type': 'application/json' }
        )
      }
    );
  }
}
