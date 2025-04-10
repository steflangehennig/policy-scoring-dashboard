import { useState } from 'react';
import './ProfileCard.css';


// src/ProfileCard.js

function ProfileCard(props) {
    const [likes, setLikes] = useState(0);
  
    return (
      <div className="card">
        <h2>{props.name}</h2>
        <p>{props.title}</p>
        <button onClick={() => setLikes(likes + 1)}>👍 Like ({likes})</button>
      </div>
    );
  }

export default ProfileCard;
