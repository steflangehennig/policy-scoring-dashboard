import { useState } from 'react';
import ProfileCard from './ProfileCard';

function App() {
  const [name, setName] = useState('Dr. Langehennig');
  const [title, setTitle] = useState('BIA Faculty, Daniels School of Business');

  return (
    <div>
      <h1>Faculty Profile</h1>

      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <br />
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <ProfileCard name={name} title={title} />
    </div>
  );
}

export default App;
