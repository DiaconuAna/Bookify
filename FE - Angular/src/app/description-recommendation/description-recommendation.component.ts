import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {faSearch} from "@fortawesome/free-solid-svg-icons";
import {MainService} from "../service/main.service";
import {Router} from "@angular/router";
import {RecommenderService} from "../service/recommender.service";
import {NgForm} from "@angular/forms";
import {searchBook} from "../model/search_book";
import {fromEvent} from "rxjs";
import {TopNavigationComponent} from "../top-navigation/top-navigation.component";

@Component({
  selector: 'app-description-recommendation',
  templateUrl: './description-recommendation.component.html',
  styleUrls: ['./description-recommendation.component.css']
})
export class DescriptionRecommendationComponent implements OnInit {

  @ViewChild(TopNavigationComponent) topNav: TopNavigationComponent | undefined;
  @ViewChild('myForm') form: NgForm | undefined;
  @ViewChild('list') list: ElementRef | undefined;

  searchIcon = faSearch;
  title!: string;
  criteria!: string;
  search_text!: string;
  topBooks = 5;
  recommendedBooks!: searchBook[];
  isLoading = false;
  showList = false;

  constructor(private bookService: MainService, private router: Router  , private recService: RecommenderService) {
    fromEvent(document, 'click').subscribe(() => {
      // @ts-ignore
      this.topNav?.showList = false;
    });
  }

  ngOnInit(): void {
  }

  searchBook(book_id: string) {
    this.router.navigate(['/book', book_id])
  }

  onSubmit() {
    // @ts-ignore
    this.isLoading = true
    // @ts-ignore
    let formText = this.form.value.search_text;
    this.search_text = formText;
    formText = formText.replaceAll(' ', '+')
    console.log(formText)
    this.criteria = this.form?.value.criteria;
    this.recService.getRecommendationsModel1(formText, this.criteria, this.topBooks).subscribe(
      res => {
        console.log(res)
        this.recommendedBooks = res['recommendations']
        this.isLoading = false;
      },
      error => {
        console.log(error)
        this.isLoading = false;
      }
    )
  }

  onSelected(value: string): void {
    this.topBooks = parseInt(value);
  }

}
