import './styles/trip-card.css';

export type Trip = { id: string; title: string; dates: string; photoUrl: string; photoAlt: string };

export function TripCard({ trip }: { trip: Trip }) {
  return (
    <article className="trip-card trip-card--photo">
      <div>
        <h3 className="trip-card__title">{trip.title}</h3>
        <p className="trip-card__dates">{trip.dates}</p>
      </div>
      <img className="trip-card__thumb" src={trip.photoUrl} alt={trip.photoAlt} />
    </article>
  );
}
