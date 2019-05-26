import { StatsInfo } from './stats_info';
import { Count } from './count';

interface User {
  id: number;
  name: string;
  icon: string;
}

export interface UserStats {
  id: number;
  userId: string;
  name: string;
  all: number;
  done: number;
  byStatus: Array<Count>;
  byCategories: Array<Count>;
  wiki: number;
  stars: number;
  actualAvgTime: number;
  // oftenTogetherUser: User;
}

export interface MemberStats {
  statsInfo: StatsInfo;
  users: Array<UserStats>;
}
