import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HeaderComponent } from "./components/header/header.component";
import { FeaturesComponent } from './components/features/features.component';
import { FooterComponent } from "./components/footer/footer.component";
import { TheaterSelectionComponent } from "./components/theater-selection/theater-selection.component";
import { HighlightsComponent } from "./components/highlights/highlights.component";
import { AdditionalInfoComponent } from "./components/additional-info/additional-info.component";
import { NotesComponent } from "./components/notes/notes.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HeaderComponent, FeaturesComponent, FooterComponent, TheaterSelectionComponent, HighlightsComponent, AdditionalInfoComponent, NotesComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'bigbash';
}
