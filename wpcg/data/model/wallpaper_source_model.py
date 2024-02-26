# wpcg-py, a simple wallpaper changer
# Copyright (C) 2023  JakobPer
# 
# Full notice in Readme.md

from typing import Any, List, Optional
from sqlalchemy import String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class WallpaperSourceModel(Base):
    """
    Defines a wallpaper source entry.
    """
    __tablename__ = "wallpaper_source"

    sid: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    enabled: Mapped[bool] = mapped_column(default=True)

    history: Mapped[List["HistoryModel"]] = relationship(back_populates="wallpaper_source", cascade="all, delete-orphan") # back populates 'wallpaper_source' of the HistoryModel

    def __init__(self, url: str, enabled=True):
        """
        Initializes the entry.

        :param sid: the id of the source entry
        :param url: the url of the source entry
        :param enabled: if the source should be enabled
        """
        super().__init__(url = url, enabled = enabled)

class HistoryModel(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    entry: Mapped[str]
    is_ignored: Mapped[bool] = mapped_column(default=False)
    wallpaper_source_id: Mapped[int] = mapped_column(ForeignKey("wallpaper_source.sid"))
    wallpaper_source: Mapped["WallpaperSourceModel"] = relationship(back_populates="history")

    def __init__(self, entry: str, wallpaper_source: WallpaperSourceModel, is_ignored = False):
        super().__init__(entry = entry, wallpaper_source = wallpaper_source, is_ignored = is_ignored)
