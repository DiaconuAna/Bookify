import { Component, OnInit } from '@angular/core';
import {NgbActiveModal} from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-modal-shelf-confirmation',
  templateUrl: './modal-shelf-confirmation.component.html',
  styleUrls: ['./modal-shelf-confirmation.component.css']
})
export class ModalShelfConfirmationComponent implements OnInit {

  someInput: string | undefined;

  constructor(public activeModal: NgbActiveModal) {}

  close(result: string) {
    this.activeModal.close(result);
  }

  dismiss(reason: string) {
    this.activeModal.dismiss(reason);
  }

  ngOnInit(): void {
  }
}

