from src import run_extraction_and_clustering
from UI import plot

def main(productID):
    #try:
        df = run_extraction_and_clustering.main(productID)
        plot.main(df,1,productID)
    #except:
     #   print()
      #  df = {}
       # plot.main(df,0,productID)


if __name__ == "__main__":
    main("B07JK98NNQ")