from sqlalchemy import create_engine, Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    url = Column(String, primary_key=True)
    prices = relationship(
	    "PriceHistory", back_populates="product", cascade="all, delete-orphan"
	)


class PriceHistory(Base):
    __tablename__ = "price_histories"

    id = Column(String, primary_key=True)
    product_url = Column(String, ForeignKey("products.url"))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    main_image_url = Column(String)
    time = Column(DateTime, nullable=False)
    product = relationship("Product", back_populates="prices")

class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_product(self, url):
        session = self.Session()
        try:
            #Create the product entry
            product = Product(url=url)
            session.merge(product) # merge will update if exists, insert if not
            session.commit()
        finally:
            session.close()

    def add_price(self, product_data):
        session = self.Session()
        try:
            session.merge(Product(url=product_data["url"]))
            price_history = PriceHistory(
                    id=f"{product_data['url']}_{product_data['time']}",
                    product_url=product_data["url"],
                    name=product_data["name"],
                    price=product_data["price"],
                    currency=product_data["currency"],
                    time=product_data["time"],
            )
            session.add(price_history)
            session.commit()
        except Exception as e:
            print(f"Error during add_price transaction for {product_data.get('url')}: {e}")
            session.rollback()
            raise
        finally:
            session.close()
