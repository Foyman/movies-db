class HomeController < ApplicationController
  def index
    @genre_list = ["Action", "Adventure", "Animated", "Biography",
              "Comedy", "Crime", "Documentary","Drama", "Epic", "Family",
              "Fantasy", "History", "Horror", "Independent", "Musical", "Mystery",
              "Political", "Romance", "Science-Fiction", "Silent", "Sport",
              "Thriller", "Western", "War"]

    @movie_query = MovieQuery.new
  end

  def movie
    puts "#{@movie_query}"
    #@movie_title = "Movie Title"
    #@movie_year = "Year"
    #@movie_length = "Length"
    #@movie_genres = "Genres"
    #@movie_won = "Win"
  end
end
