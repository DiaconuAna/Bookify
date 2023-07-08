import {Component, ElementRef, OnInit, PipeTransform, ViewChild} from '@angular/core';
import {MainService} from "../service/main.service";
import {Router} from "@angular/router";
import {RecommenderService} from "../service/recommender.service";
import {fromEvent} from "rxjs";
import {TopNavigationComponent} from "../top-navigation/top-navigation.component";
import {NgForm} from "@angular/forms";
import {Sentiment} from "../model/sentiment";
import Chart from "chart.js/auto";
import {SentimentBook} from "../model/sentiment-book";

@Component({
  selector: 'app-user-profile-recommendation',
  templateUrl: './user-profile-recommendation.component.html',
  styleUrls: ['./user-profile-recommendation.component.css']
})
export class UserProfileRecommendationComponent implements OnInit {

  @ViewChild(TopNavigationComponent) topNav: TopNavigationComponent | undefined;
  @ViewChild('myForm') form: NgForm | undefined;
  @ViewChild('list') list: ElementRef | undefined;


  public chart: any;
  sentimentStatistic!: Sentiment[];
  recommendedBooks!: SentimentBook[];
  filteredBooks!: SentimentBook[];
  selectedSentiments: string[] = [];
  allSentiments: string[] = ['acceptance', 'anger', 'annoyance', 'anxiety', 'bliss', 'calmness', 'delight', 'disgust', 'dislike', 'delight', 'eagerness', 'ecstasy', 'enthusiasm', 'fear', 'grief', 'joy', 'loathing', 'melancholy', 'pleasantness', 'rage', 'responsiveness', 'sadness', 'serenity', 'terror'];
  checkedValues: boolean[] = Array(25).fill(false);
  totalWeight = 0;

  isLoading = true;
  hasInfo = false;

  constructor(private bookService: MainService, private router: Router, private recService: RecommenderService) {
    fromEvent(document, 'click').subscribe(() => {
      // @ts-ignore
      this.topNav?.showList = false;
    });
  }

  search(text: string, pipe: PipeTransform): SentimentBook[] {
    return this.recommendedBooks.filter((book) => {
      const term = text.toLowerCase();
      return (
        book.title.toLowerCase().includes(term) ||
        pipe.transform(book.id).includes(term) ||
        book.sentiments.toLowerCase().includes(term)
      );
    });
  }

  ngOnInit(): void {
    this.profileRecommendation();
  }

  profileRecommendation() {
    let username = ""
    if (localStorage.getItem('username') != null) { // @ts-ignore
      username = localStorage.getItem('username')
    }
    this.recService.getUserProfileRecommendations(username).subscribe(
      res => {
        this.isLoading = false;
        if(res.recommendations.books.length == 0){
          this.hasInfo = false;
        }
        else {
          this.recommendedBooks = res.recommendations.books
          this.sentimentStatistic = res.recommendations.sentiments
          this.filteredBooks = this.recommendedBooks;
          this.hasInfo = true;
          this.totalWeight = this.sentimentStatistic.reduce((totalWeight, sentiment) => totalWeight + Number(sentiment.weight), 0);
          this.createChart()
        }
      },
      error => {
        console.log(error)
      }
    )
  }

  createChart() {
  console.log(this.sentimentStatistic)
    this.chart = new Chart("SentimentStatistic", {
      type: 'pie', //this denotes the type of chart
      data: {// values on X-Axis
        labels: [this.sentimentStatistic[0].sentiment, this.sentimentStatistic[1].sentiment,
          this.sentimentStatistic[2].sentiment, this.sentimentStatistic[3].sentiment,
          this.sentimentStatistic[4].sentiment, 'Other',],
        datasets: [{
          label: 'Percentage',
          data: [Number(this.sentimentStatistic[0].weight), Number(this.sentimentStatistic[1].weight), Number(this.sentimentStatistic[2].weight),
            Number(this.sentimentStatistic[3].weight), Number(this.sentimentStatistic[4].weight), 100 - this.totalWeight],
          backgroundColor: [
            'red',
            'pink',
            'green',
            'yellow',
            'orange',
            'blue',
          ],
          hoverOffset: 4
        }],
      },
      options: {
        aspectRatio: 2.5,
        plugins:{
          legend: {
            position: "bottom",
            align: "center",
          },
          title:{
            display: true,
            text: "User Profile Sentiment Distribution",
          },
        },
      },
    });
  }

  onCheckboxChange(sentiment: string, isChecked: boolean) {
    console.log(isChecked, sentiment)
    if (isChecked) {
      this.selectedSentiments.push(sentiment);
    } else {
      const index = this.selectedSentiments.indexOf(sentiment);
      this.selectedSentiments.splice(index, 1);
    }
    this.filterByEmotion();
  }

  filterByEmotion(){
    console.log(this.selectedSentiments)
    this.filteredBooks = this.recommendedBooks.filter((book: SentimentBook) => {
      if (this.selectedSentiments.length === 0) {
        return this.recommendedBooks; // show all items if no category is selected
      } else {
        const bookSentiments = book.sentiments.toLowerCase().split(',');
        return this.selectedSentiments.some(category => bookSentiments.includes(category.toLowerCase()));
      }
    });
    console.log(this.filteredBooks)
  }
}
