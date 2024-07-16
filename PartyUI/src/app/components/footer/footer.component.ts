import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent {
  notes = [
    { title: 'Food & Beverages', description: 'Enjoy delicious in-theatre dining options at affordable prices!' },
    { title: 'Screening', description: 'Bring your own OTT accounts and relive the theatre magic!' },
    { title: 'Cakes', description: 'Choose the perfect cake for your celebration from our selection.' },
    { title: 'Bouquets', description: 'Add a beautiful rose bouquet to enhance your celebration.' }
  ];
}