import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';
import { io, Socket } from 'socket.io-client';
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Stack';
import Button from '@mui/material/Button';

import Cleave from 'cleave.js/react';
const ENDPOINT="http://localhost:5000"
const imageUrls = [
  "https://logos-world.net/wp-content/uploads/2020/04/Visa-Logo.png",
  "https://brand.mastercard.com/content/dam/mccom/brandcenter/thumbnails/mastercard_vrt_rev_92px_2x.png",
  "https://www.discover.com/company/images/newsroom/media-downloads/discover.png",
  "https://s1.q4cdn.com/692158879/files/design/svg/american-express-logo.svg",
  "https://cdn4.iconfinder.com/data/icons/simple-peyment-methods/512/diners_club-512.png",
  "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/JCB_logo.svg/1280px-JCB_logo.svg.png"
]

// const socket = io(ENDPOINT);

function App() {
  const [creditCardNum, setCreditCardNum] = useState('#### #### #### ####');
  const [cardType, setCardType] = useState('')
  const [cardHolder, setCardHolder] = useState('Your Full Name');
  const [expireMonth, setExpireMonth] = useState('MM');
  const [expireYear, setExpireYear] = useState('YYYY');
  const [cardTypeUrl, setCardTypeUrl] = useState('https://logos-world.net/wp-content/uploads/2020/04/Visa-Logo.png');

  // const [isConnected, setIsConnected] = useState(socket.connected);
  const [lastPong, setLastPong] = useState(null);
  const socket = io(ENDPOINT);

  const handleNum = (e) => {
    setCreditCardNum(e.target.rawValue);
    // console.log(e.target.value);
  }
  useEffect(() => {
    console.log('lol')
    socket.on('update_card', function(message) { 
      console.log(message)
      if (message.expiration !== null)
      {
        const answer_array = message.expiration.split('/');
        setExpireMonth(answer_array[1])
        setExpireYear('20' + answer_array[0])
      }
      if (message.type !== null) {
        handleType(message.type)
      }
      if (message.card_number !== null){
        setCreditCardNum(message.card_number)
      }
    })
  }, [expireYear, creditCardNum])
  const handleType = (type) => {
    setCardType(type);
    console.log(type);

  const handleClick = () => {
    // socket.emit('get_card', 'get_card');
    console.log("click");
  }
  const handleClose = () => {
    // setLastPong(null);
    console.log("close");
  }


    if(type === "visa") {
      setCardTypeUrl(imageUrls[0]);
      console.log("Visa")
    } else if(type === "mastercard") {
      setCardTypeUrl(imageUrls[1]);
      console.log("Mastercard")
    } else if(type === "discover") {
      setCardTypeUrl(imageUrls[2]);
      console.log("Discover")
    } else if(type === "amex") {
      setCardTypeUrl(imageUrls[3]);
      console.log("Amex")
    } else if(type === "diners") {
      console.log("Diners")
      setCardTypeUrl(imageUrls[4])
    } else if(type === "jcb") {
      console.log("JCB");
      setCardTypeUrl(imageUrls[5]);
    }
  }
  
  const handleCardHolder = (e) => {
    setCardHolder(e.target.value);
  }

  const handleExpMonth = (e) => {
    setExpireMonth(e.target.value);
  }

  const handleExpYear = (e) => {
    setExpireYear(e.target.value);
  }

  useEffect(() => {
    return () => {
      socket?.disconnect();
  
    }
  }, [socket])

  return (
    <div className="container">
     <form id="form">
         <div id="card">
             <div className="header">
                 <div className="sticker"></div>
                 <div>
                   <img className="logo" src={cardTypeUrl} alt="Card logo"/>
                 </div>
             </div>
             <div className="body">
                 <h2 id="creditCardNumber">{creditCardNum}</h2>
             </div>
             <div className="footer">
                 <div>
                     <h5>Card Holder</h5>
                     <h3>{cardHolder}</h3>
                 </div>
                 <div>
                     <h5>Expires</h5>
                     <h3>{expireMonth} / {expireYear}</h3>
                 </div>
             </div>
         </div>

      <div className="input-container mt">
        <h4>test</h4>
        <Button variant="outlined" >
  Card information details
</Button>
<Snackbar  autoHideDuration={6000} >
  
</Snackbar>
<Alert severity="error">This is an error message!</Alert>
<Alert severity="warning">This is a warning message!</Alert>
<Alert severity="info">This is an information message!</Alert>
<Alert severity="success">This is a success message!</Alert>
      </div>
         {/* <div className="input-container mt">
             <h4>Enter card number</h4>
             <Cleave
               delimiter="-"
               options={{
                 creditCard: true,
                 onCreditCardTypeChanged: handleType
               }}
               onChange={handleNum}
               placeholder="Please enter your credit card number"
             />
         </div> */}

         <div className="input-container">
         </div>

         <div className="input-grp">
             <div className="input-container">
                 {/* <input type="" placeholder="CVV" required/> */}
             </div>
         </div>
              </form>
 </div>
);
}

export default App;
