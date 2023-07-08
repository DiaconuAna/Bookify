import {Component, ElementRef, Input, OnInit, ViewChild} from '@angular/core';
import {faSearch} from "@fortawesome/free-solid-svg-icons";
import {bookTitle} from "../model/book_title";
import {MainService} from "../service/main.service";
import {ActivatedRoute, Router} from "@angular/router";
import {NgbModal} from "@ng-bootstrap/ng-bootstrap";
import {fromEvent} from "rxjs";
import {Rating} from "../model/rating";
import {TopNavigationComponent} from "../top-navigation/top-navigation.component";

@Component({
  selector: 'app-book-review-page',
  templateUrl: './book-review-page.component.html',
  styleUrls: ['./book-review-page.component.css']
})
export class BookReviewPageComponent implements OnInit {

  @ViewChild(TopNavigationComponent) topNav: TopNavigationComponent | undefined;
  @ViewChild('list') list: ElementRef | undefined;

  searchIcon = faSearch;
  title!: string;
  searchedBookTitles!: bookTitle[];

  defaultImage = 'https://upload.wikimedia.org/wikipedia/commons/b/b9/No_Cover.jpg?20090511140841';
  @Input() bookReviews!: Rating[];
  pagedBookReviews!: Rating[]
  userBookReviews!: Rating[]
  isLoading = true;

  showList = false;
  page = 1;
  pageCount = 0;

  constructor(private bookService: MainService, private router: Router, private route: ActivatedRoute, private modalService: NgbModal) {
    route.params.subscribe(val => {
        this.searchedBookTitles = []
        this.getAllReviews()
      },
      error => {
        console.log(error)
      });

    fromEvent(document, 'click').subscribe(() => {
      // @ts-ignore
      this.topNav?.showList = false;
    });

  }

  ngOnInit(): void {
  }

  getAllReviews() {
    this.bookService.getBookReviews(this.route.snapshot.params['title']).subscribe(
      res => {
        this.bookReviews = res

        this.pageCount = Math.floor(res.length / 10);
        if (res.length % 10) {
          this.pageCount++;
        }
        this.getPageInfo()
        this.getUserReviewsV2()
        this.isLoading = false

      },
      error => {
        console.log(error)
      }
    )
  }

  getUserReviewsV2(){
    this.userBookReviews = this.bookReviews.filter((review) => review.profile_name === localStorage.getItem('username'))
  }

  getUserReviews() {
    let username = ""
    if (localStorage.getItem('username') != null) { // @ts-ignore
      username = localStorage.getItem('username')
    }
    this.bookService.getUserReviews(username, this.route.snapshot.params['title']).subscribe(
      res => {
        this.userBookReviews = res
      },
      error => {
        console.log(error)
      }
    )
  }

  getPageInfo() {
    if (this.pageCount == this.page) {
      this.pagedBookReviews = this.bookReviews.slice(-(this.bookReviews.length % 10))
    } else {
      let startIndex = (this.page - 1) * 10
      let endIndex = (this.page * 10);
      this.pagedBookReviews = this.bookReviews.slice(startIndex, endIndex)
    }
  }

  ShowReviewPolarity(review_id: number){
    this.bookService.getReviewPolarity(review_id).subscribe(
      res =>{
        console.log(res)
        let review = this.bookReviews.find(item => item.id == review_id)
        // @ts-ignore
        review.showPolarity = true
        // @ts-ignore
        review.polarity = res.polarity
        // @ts-ignore
        review.emotions = res.sentiments.substring(1, res.sentiments.length - 1).replace(/'/g, "")
      },
      error => {
        console.log(error)
      }

    )
  }

  HideReviewPolarity(review_id: number){
    let review = this.bookReviews.find(item => item.id == review_id)
    // @ts-ignore
    review.showPolarity = false
  }

  get oneStarCount(): number {
    return this.bookReviews.filter(review => review.score >= 0 && review.score < 1.5).length;
  }

  get twoStarCount(): number {
    return this.bookReviews.filter(review => review.score >= 1.5 && review.score < 2.5).length;
  }

  get threeStarCount(): number {
    return this.bookReviews.filter(review => review.score >= 2.5 && review.score < 3.5).length;
  }

  get fourStarCount(): number {
    return this.bookReviews.filter(review => review.score >= 3.5 && review.score < 4.5).length;
  }

  get fiveStarCount(): number {
    return this.bookReviews.filter(review => review.score >= 4.5 && review.score <= 5).length;
  }

  get totalCount(): number {
    return this.bookReviews.length;
  }

  get oneStarPercentage(): number {
    return this.oneStarCount / this.totalCount * 100;
  }

  get twoStarPercentage(): number {
    return this.twoStarCount / this.totalCount * 100;
  }

  get threeStarPercentage(): number {
    return this.threeStarCount / this.totalCount * 100;
  }

  get fourStarPercentage(): number {
    return this.fourStarCount / this.totalCount * 100;
  }

  get fiveStarPercentage(): number {
    return this.fiveStarCount / this.totalCount * 100;
  }
}
