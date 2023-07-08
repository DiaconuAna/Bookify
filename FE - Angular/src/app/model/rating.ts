export interface Rating{
  id: number;
  profile_name: string;
  review_summary: string;
  review_text: string;
  score: number;
  user_id: string;
  polarity: number;
  emotions: string;
  showPolarity: boolean;
}
