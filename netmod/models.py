



import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BaseNetMod:

    def __iter__(self):
        for v in self.values:
            yield v, getattr(self, v)

    def get_type(self):
        return self.__tablename__

    def get_keys(self):
        return {pk.name: getattr(self, pk.name) for pk in self.__table__.primary_key}

    def get_attrs(self):
        return {attr: getattr(self, attr) for attr in self.attributes}


class Site(Base, BaseNetMod):
    """
    """

    __tablename__ = "site"

    childs = ["devices"]
    attributes = []

    name = Column(String(250), primary_key=True)
    devices = relationship("Device", back_populates="site")

    def __repr__(self):
        return f"{self.name}"

class Device(Base, BaseNetMod):
    """
    """

    __tablename__ = "device"

    childs = ["interfaces"]
    attributes = []

    name = Column(String(250), primary_key=True)
    site_name = Column(String(250), ForeignKey("site.name"), nullable=True)
    site = relationship("Site", back_populates="devices")
    interfaces = relationship("Interface", back_populates="device")

    def __repr__(self):
        return f"{self.name}"

class Interface(Base, BaseNetMod):
    """
    """

    __tablename__ = "interface"

    childs = ["ips"]
    attributes = ["description", "mtu", "switchport_mode"]

    name = Column(String(250), primary_key=True)
    description = Column(String(250), nullable=True)
    mtu = Column(Integer, nullable=True)
    switchport_mode = Column(String(250), nullable=True)

    device_name = Column(Integer, ForeignKey("device.name"), nullable=False, primary_key=True)
    device = relationship("Device", back_populates="interfaces")
    ips = relationship("IPAddress")

    def __repr__(self):
        return f"{self.device_name}::{self.name}"

class IPAddress(Base, BaseNetMod):
    """
    """

    __tablename__ = "ip_address"

    childs = []
    attributes = []

    address = Column(String(250), primary_key=True)
    interface_name = Column(String(250))
    device_name = Column(String(250))

    __table_args__ = (
        ForeignKeyConstraint(
            ['device_name', 'interface_name'],
            ['interface.device_name', 'interface.name'],
        ),
    )

    def __repr__(self):
        return f"{self.address}"

class Cable(Base, BaseNetMod):
    """
    """

    __tablename__ = "cable"

    childs = []
    attributes = []

    id = Column(Integer, primary_key=True)
    device_a_name = Column(String(250))
    interface_a_name = Column(String(250))
    device_z_name = Column(String(250))
    interface_z_name = Column(String(250))

    __table_args__ = (
        ForeignKeyConstraint(
            ['device_a_name', 'interface_a_name', 'device_z_name', 'interface_z_name'],
            ['interface.device_name', 'interface.name', 'interface.device_name', 'interface.name'],
        ),
    )

    def __repr__(self):
        return f"Cable {self.device_a_name}::{self.interface_a_name} {self.device_z_name}::{self.interface_z_name}"

# class Optic(Base):
#     """
#     """

#     __tablename__ = "optic"

#     id = Column(Integer, primary_key=True)
#     serial = Column(String(250), nullable=True)
#     interface = Column(Integer, ForeignKey("interface.id"), nullable=True)

# class Vlan(Base):
#     """
#     """

#     __tablename__ = "vlan"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=True)
#     vid = Column(Integer, nullable=True)

# class Prefix(Base):
#     """
#     """

#     __tablename__ = "prefix"

#     id = Column(Integer, primary_key=True)
#     prefix = Column(String(250), nullable=True)