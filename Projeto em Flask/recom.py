from textwrap import indent
import animes_list

animes_names_index = animes_list.ANIMES_LIST

def get_recommended_animes(suggestions):
    animes_names = []
    for i in range(len(suggestions)):
      animes_names.append(animes_names_index[suggestions[i]])
    return animes_names