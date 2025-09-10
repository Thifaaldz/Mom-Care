from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Tuple, Dict
import pandas as pd
import geojson, heapq
from collections import defaultdict
from math import radians, sin, cos, asin, sqrt
import os

app = FastAPI(title="Rute Bidan API")

# allow CORS untuk Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Utility fungsi =====
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1); dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def load_graph_from_geojson(path: str):
    with open(path, "r", encoding="utf-8") as f:
        gj = geojson.load(f)
    features = gj["features"]

    min_lon, max_lon = 106.6, 107.0
    min_lat, max_lat = -6.4, -6.05

    def inside_jakarta(lon, lat):
        return (min_lon <= lon <= max_lon) and (min_lat <= lat <= max_lat)

    nodes, rev_nodes, adj = {}, {}, defaultdict(list)

    def get_id(lat, lon):
        key = (round(lat,6), round(lon,6))
        if key not in nodes:
            idx = len(nodes)
            nodes[key] = idx
            rev_nodes[idx] = key
        return nodes[key]

    for feat in features:
        geom = feat["geometry"]; coords = geom["coordinates"]
        if geom["type"] == "LineString":
            for i in range(len(coords)-1):
                lon1, lat1 = coords[i][:2]
                lon2, lat2 = coords[i+1][:2]
                if not (inside_jakarta(lon1, lat1) and inside_jakarta(lon2, lat2)):
                    continue
                u, v = get_id(lat1, lon1), get_id(lat2, lon2)
                w = haversine_km(lat1, lon1, lat2, lon2)
                adj[u].append((v,w)); adj[v].append((u,w))
        elif geom["type"] == "MultiLineString":
            for line in coords:
                for i in range(len(line)-1):
                    lon1, lat1 = line[i][:2]
                    lon2, lat2 = line[i+1][:2]
                    if not (inside_jakarta(lon1, lat1) and inside_jakarta(lon2, lat2)):
                        continue
                    u, v = get_id(lat1, lon1), get_id(lat2, lon2)
                    w = haversine_km(lat1, lon1, lat2, lon2)
                    adj[u].append((v,w)); adj[v].append((u,w))

    return nodes, rev_nodes, adj

def nearest_node(lat: float, lon: float, rev_nodes: Dict[int, Tuple[float,float]]):
    best, best_d = None, float("inf")
    for idx, (nlat,nlon) in rev_nodes.items():
        d = haversine_km(lat, lon, nlat, nlon)
        if d < best_d:
            best, best_d = idx, d
    return best

def dijkstra(adj: Dict[int, List[Tuple[int,float]]], source: int, target: int):
    pq = [(0.0, source)]
    dist, prev, visited = {source:0.0}, {}, set()
    while pq:
        d,u = heapq.heappop(pq)
        if u in visited: continue
        visited.add(u)
        if u == target: break
        for v,w in adj.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq,(nd,v))
    if target not in dist:
        return float("inf"), []
    path=[target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    return dist[target], list(reversed(path))

# ===== Init (load data once at startup) =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GEOJSON_PATH = os.path.join(BASE_DIR, "Jaringan_jalanan_indonesia.geojson")
BIDAN_CSV_PATH = os.path.join(BASE_DIR, "bidan_points.csv")

# contoh CSV jika belum ada
if not os.path.exists(BIDAN_CSV_PATH):
    default_bidan = pd.DataFrame([
        [1,"Bidan Sari",-6.2005,106.8233,4.8,"Jl. Melati 1","0812-1111-1111"],
        [2,"Bidan Dewi",-6.2091,106.8292,4.7,"Jl. Kenanga 2","0812-2222-2222"],
        [3,"Bidan Ayu",-6.2173,106.8325,4.9,"Jl. Mawar 3","0812-3333-3333"],
    ], columns=["id","name","lat","lon","rating","address","phone"])
    default_bidan.to_csv(BIDAN_CSV_PATH, index=False)

nodes, rev_nodes, adj = load_graph_from_geojson(GEOJSON_PATH)
bidan_df = pd.read_csv(BIDAN_CSV_PATH)

# ===== Endpoints =====
@app.get("/")
def root():
    return {"message": "Rute Bidan API berjalan"}

@app.get("/bidan_list")
def get_bidan_all():
    return bidan_df.to_dict(orient="records")

@app.get("/route")
def get_route(user_lat: float, user_lon: float, bidan_id: int):
    matches = bidan_df[bidan_df["id"] == bidan_id]
    if matches.empty:
        raise HTTPException(status_code=404, detail="Bidan tidak ditemukan")

    dest_row = matches.iloc[0]
    dest_lat, dest_lon = float(dest_row["lat"]), float(dest_row["lon"])

    s_id = nearest_node(user_lat, user_lon, rev_nodes)
    t_id = nearest_node(dest_lat, dest_lon, rev_nodes)

    if s_id is None or t_id is None:
        raise HTTPException(status_code=500, detail="Tidak dapat menemukan node terdekat")

    dist_km, path_ids = dijkstra(adj, s_id, t_id)

    if not path_ids:
        straight = haversine_km(user_lat, user_lon, dest_lat, dest_lon)
        return {
            "dist_km": straight,
            "path": [
                {"lat": user_lat, "lon": user_lon},
                {"lat": dest_lat, "lon": dest_lon},
            ],
            "dest": {"lat": dest_lat, "lon": dest_lon},
        }

    route_points = [
        {"lat": rev_nodes[nid][0], "lon": rev_nodes[nid][1]} for nid in path_ids
    ]

    return {
        "dist_km": dist_km,
        "path": route_points,
        "dest": {"lat": dest_lat, "lon": dest_lon},
    }
