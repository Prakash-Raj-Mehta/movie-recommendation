import streamlit as st
import pickle
import pandas as pd

import requests
st.markdown("""
<style>
    /* Hide Streamlit default header */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Button container - fixed top right */
    .dev-profile-btn {
        margin-top: 80px;
        position: fixed;
        top: 18px;
        right: 28px;
        z-index: 9999;
    }

    .dev-profile-btn a {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        text-decoration: none !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-size: 14px;
        font-weight: 600;
        
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        letter-spacing: 0.3px;
    }

    .dev-profile-btn a:hover {
        cursor: pointer;
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.55);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    .dev-profile-btn a:active {
        transform: translateY(-1px) scale(0.98);
    }

    /* Optional subtle pulse animation on load */
    @keyframes softPulse {
        0% { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
        50% { box-shadow: 0 4px 22px rgba(102, 126, 234, 0.6); }
        100% { box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); }
    }

    .dev-profile-btn a {
        animation: softPulse 2.5s ease-in-out infinite;
    }

    .dev-profile-btn a:hover {
        animation: none;
    }
</style>

<div class="dev-profile-btn">
    <a href="https://prakash-raj-mehta.github.io/portfolio/" target="_blank">
        👨‍💻 View Developer Profile
    </a>
</div>
""", unsafe_allow_html=True)

# ---- Your app content starts here ----
st.title("Welcome to My App")

# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
#     data = response.json()

#     return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]


# import requests
# import streamlit as st

@st.cache_data(ttl=3600)  
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    
   
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
            
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
    
   
    return "https://via.placeholder.com/500x750?text=No+Poster+Available"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies =[]
    recommeded_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommeded_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommeded_movies_posters

similarity = pickle.load(open('similarity.pkl','rb'))
# movies = pickle.load(open('movies.pkl','rb'))

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
# movies= movies_dict['title'].values

st.title('Movie Recommendation')

selected_movie_name = st.selectbox(
    'recomended movies ',
    movies['title'].values
)
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])



