import { StatsInfo } from './stats_info';
import { Count } from './count';

export interface IssueStats {
  statsInfo: StatsInfo;
  all: number;
  done: number;
  byStatus: Array<Count>;
  byCategories: Array<Count>;
  wiki: number;
  stars: number;
  actualAvgTime: number;
}
