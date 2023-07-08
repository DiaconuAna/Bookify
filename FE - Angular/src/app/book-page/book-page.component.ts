import {AfterViewInit, Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MainService} from "../service/main.service";
import {ActivatedRoute, Router} from "@angular/router";
import {faSearch} from "@fortawesome/free-solid-svg-icons";
import {bookTitle} from "../model/book_title";
import {Book} from "../model/book";
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';
import {fromEvent} from 'rxjs';
import {ModalShelfConfirmationComponent} from "../modal-shelf-confirmation/modal-shelf-confirmation.component";
import {TopNavigationComponent} from "../top-navigation/top-navigation.component";
import {ModalUserReviewComponent} from "../modal-user-review/modal-user-review.component";

@Component({
  selector: 'app-book-page',
  templateUrl: './book-page.component.html',
  styleUrls: ['./book-page.component.css']
})
export class BookPageComponent implements OnInit {
  @ViewChild(TopNavigationComponent) topNav: TopNavigationComponent | undefined;
  @ViewChild('list') list: ElementRef | undefined;

  searchIcon = faSearch;
  title!: string;
  searchedBookTitles!: bookTitle[];

  defaultImage = 'https://upload.wikimedia.org/wikipedia/commons/b/b9/No_Cover.jpg?20090511140841';
  currentBook!: Book;
  isLoading = true;
  showSentiments = false;

  sentiment_list= [];
  keywords_list!: string[];
  original_author!: string;

  constructor(private bookService: MainService, private router: Router, private route: ActivatedRoute, private modalService: NgbModal) {
    route.params.subscribe(val => {
        this.searchedBookTitles = []
        this.bookService.findBookByTitle(this.route.snapshot.params['title']).subscribe(
          res => {
            this.currentBook = res;
            this.original_author = this.currentBook.authors;
            this.currentBook.authors = this.currentBook.authors.replaceAll("'","")
            if (this.currentBook.keywords.length > 0){
              this.keywords_list = this.currentBook.keywords.split(",")
            }
            else{
              this.keywords_list = []
            }
            this.isLoading = false;
          },
          error => {
            console.log(error)
          }
        )
      this.bookService.getBookSentiments(this.route.snapshot.params['title']).subscribe(
        res => {
          if(res.sentiments.length == 0) {
            this.sentiment_list = [];
          }
          else {
            this.sentiment_list = res.sentiments[0].substring(1, res.sentiments[0].length - 1).split(",");
          }
          console.log(this.sentiment_list)
        },
        error => {
          console.log(error)
        }
      )
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

  openReviewModal(username: string, shelf: string){
    const modalRef = this.modalService.open(ModalUserReviewComponent);
    modalRef.result.then((result) => {
      console.log(result)
        this.bookService.addBookToShelf(username, this.currentBook.id, shelf).subscribe(
          res => {
            console.log("good job")
          },
          error => {
            console.log(error)
          }
        )
        this.bookService.addReview({title: this.currentBook.title, review:result.text, rating: result.rating, summary: result.summary, username:username}).subscribe(
          res =>{
            console.log("Rating added successfully")
            this.refresh()
          },
          error => {
            console.log(error)
          }
        )
      },
      (reason) => {
        console.log(reason);
      });
  }

  refresh() {
    window.location.reload();
  }

  openModal(shelf: string) {
    const modalRef = this.modalService.open(ModalShelfConfirmationComponent);
    modalRef.componentInstance.someInput = shelf;
    modalRef.result.then((result) => {
        // handle the modal result
        let username = ""
        if (localStorage.getItem('username') != null) { // @ts-ignore
          username = localStorage.getItem('username')
        }
        if(shelf == 'Read'){
          this.openReviewModal(username, shelf)
        }
        else {
          this.bookService.addBookToShelf(username, this.currentBook.id, shelf).subscribe(
            res => {
              console.log("good job")
            },
            error => {
              console.log(error)
            }
          )
        }
      },
      (reason) => {
        console.log(reason);
      });
  }

  viewReviews() {
    this.router.navigate(['/review', this.currentBook.title])
  }

  goToAuthor() {
    this.router.navigate(['/author', this.original_author])
  }

}
