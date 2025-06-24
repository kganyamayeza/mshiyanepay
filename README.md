# MshiyanePay

Started this project to learn how banking systems actually work. It's been a wild ride - from basic authentication to handling real-time transactions. Still learning, but proud of how far it's come.

## What's Working

- JWT auth (took me 3 tries to get it right 😅)
- Basic banking ops (transfers, balance checks)
- Simple financial tracking
- Transaction history
- Basic fraud checks
- Security stuff I learned along the way

## Tech I'm Using

- **Backend**: FastAPI (Python) - chose this over Flask for the async support
- **Frontend**: React + TypeScript - still getting the hang of TypeScript
- **Database**: PostgreSQL - switched from SQLite when I needed better concurrency
- **Security**: JWT, SSL - learned these the hard way
- **Other**: Custom logging - built this after debugging became a nightmare

## Project Structure

```
mshiyanepay/
├── backend/          # FastAPI stuff
│   ├── models/      # Database models
│   ├── services/    # Business logic
│   ├── utils/       # Helper functions
│   └── main.py      # Entry point
├── frontend/        # React app
│   ├── src/        # Source code
│   └── public/     # Static files
└── docs/           # My notes and docs
```

## My Learning Journey

### Security (The Hard Part)
- First tried basic auth (big mistake)
- Then JWT (took 3 attempts)
- Finally got SSL working (certificates are confusing!)
- Still learning about rate limiting

### Backend (The Fun Part)
- Started with simple endpoints
- Added database stuff
- Learned about connection pooling the hard way
- Still figuring out the best way to handle errors

### Frontend (The Pretty Part)
- Basic React at first
- Added TypeScript (still making mistakes)
- Learning about state management
- UI/UX is harder than I thought

### DevOps (The Scary Part)
- Environment variables were a pain
- Logging saved my life
- Still learning about deployment
- Security is a constant battle

## Technical Challenges I Faced

### Security Headaches
- JWT implementation was tricky
- SSL setup took forever
- Rate limiting was a puzzle
- Still working on better password hashing

### Real-time Issues
- Concurrent transactions were messy
- Race conditions are sneaky
- Data consistency is hard
- Still optimizing this part

### Performance Problems
- Database queries were slow
- Connection pooling helped
- Caching is next on my list
- Frontend needs optimization

### Debugging Nightmares
- Error tracking was a mess
- Logging saved me
- User-friendly errors are hard
- Still learning better debugging

## How to Run It

1. Get the code
```bash
git clone https://github.com/yourusername/mshiyanepay.git
```

2. Backend setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Frontend setup
```bash
cd frontend
npm install
```

4. Start everything
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm start
```

## Security Stuff I've Implemented

- JWT auth (with refresh tokens)
- SSL for secure connections
- Rate limiting (basic but working)
- Input validation
- Password hashing
- Basic audit logging
- CORS protection
- SQL injection prevention

## Current Status

Still a work in progress. Learning new things every day. Some features are rough around the edges, but it's getting better. Not production-ready yet, but getting there.

## Contact

Found a bug? Have suggestions? Email me at paulmayeza2@icloud.com

## License

MIT License - feel free to use this for learning 