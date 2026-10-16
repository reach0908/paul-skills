import './styles/trip-card.css';

export type Trip = { id: string; title: string; dates: string; photoUrl: string; photoAlt: string };

export function TripCard({ trip }: { trip: Trip }) {
  return (
    <article className="trip-card">
      <img className="trip-card__photo" src={trip.photoUrl} alt={trip.photoAlt} />
      <div className="trip-card__body">
        <h3 className="trip-card__title">{trip.title}</h3>
        <p className="trip-card__dates">{trip.dates}</p>
      </div>
    </article>
  );
}
