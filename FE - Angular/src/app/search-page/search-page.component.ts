import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MainService} from "../service/main.service";
import {Router} from "@angular/router";
import {bookTitle} from "../model/book_title";
import {faSearch} from "@fortawesome/free-solid-svg-icons";
import {NgForm} from "@angular/forms";
import {SearchService} from "../service/search.service";
import {searchBook} from "../model/search_book";
import {fromEvent} from "rxjs";
import {TopNavigationComponent} from "../top-navigation/top-navigation.component";

@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.css']
})
export class SearchPageComponent implements OnInit {

  @ViewChild(TopNavigationComponent) topNav: TopNavigationComponent | undefined;
  @ViewChild('myForm') form: NgForm | undefined;
  @ViewChild('list') list: ElementRef | undefined;
  searchIcon = faSearch;
  title!: string;
  genre!: string;
  author!: string;
  criteria!: string;
  search_text!: string;
  searchedBookTitles!: bookTitle[];
  allBooks!: searchBook[];
  page = 1;
  isLoading = false;
  showList = false;


  constructor(private bookService: SearchService, private router: Router) {
    fromEvent(document, 'click').subscribe(() => {
      // @ts-ignore
      this.topNav?.showList = false;
    });
  }

  ngOnInit(): void {
  }

  onSubmit(){
    this.criteria = this.form?.value.criteria;
    // @ts-ignore
    this.search_text = this.form.value.search_text;
    this.isLoading = true;

    switch(this.criteria){
      case 'title':
        // @ts-ignore
        this.title = this.search_text;
        break
      case 'genre':
        this.genre = this.search_text;
        break
      case 'author':
        this.author = this.search_text;
        break
      default:
        console.log(this.criteria)
        console.error("Not a valid search criteria: " + this.criteria)
    }
    this.searchByCriteria( 1, 10)

  }

  searchByTitle(title: string){
    this.showList = true;
    if(title == "")
      this.searchedBookTitles = []
    else{
      this.bookService.searchByTitle(title, 1, 10).subscribe(
        res =>{
          this.searchedBookTitles = res['titles']
        },
        error => console.log(error)
      )
    }
  }

  searchByCriteria(page: number, size: number){
    switch(this.criteria){
      case 'title':
        this.searchByTitlePaged(page, size)
        break
      case 'genre':
        this.searchByGenrePaged(page, size)
        break
      case 'author':
        this.searchByAuthorPaged(page, size)
        break
      default:
        console.error("Not a valid search criteria: " + this.criteria)
    }
  }

 searchByTitlePaged(page: number, size: number){
    // @ts-ignore
   let title = this.title
    if(title == "")
      this.allBooks = []
    else{
      this.bookService.searchByTitle(title, page, size).subscribe(
        res =>{
          this.allBooks = res['titles']
          this.isLoading = false
        },
        error => {
          console.log(error);
          this.isLoading = false;
        }
      )
    }
  }

  searchByAuthorPaged(page: number, size: number){
    // @ts-ignore
   let author = this.author
    if(author == "")
      this.allBooks = []
    else{
      this.bookService.searchByAuthor(author, page, size).subscribe(
        res =>{
          this.allBooks = res['titles']
          this.isLoading = false
        },
        error => {
          console.log(error);
          this.isLoading = false;
        }
      )
    }
  }

  searchByGenrePaged(page: number, size: number){
    // @ts-ignore
   let genre = this.genre
    if(genre == "")
      this.allBooks = []
    else{
      this.bookService.searchByGenre(genre, page, size).subscribe(
        res =>{
          this.allBooks = res['titles']
          this.isLoading = false
        },
        error => {
          console.log(error);
          this.isLoading = false;
        }
      )
    }
  }


  searchDetailed(){
    this.router.navigate(['/search'])
  }

  searchBook(book_id: string) {
    this.router.navigate(['/book', book_id])
  }

  recommendDescription(){
    this.router.navigate(['/descriptionRec'])
  }

}
