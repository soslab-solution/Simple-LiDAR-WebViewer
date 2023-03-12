function DataHandler(props) {
  const [validDataset, setValidDataset] = useState(false);
  const [datasetInfo, setDatasetInfo] = useState({
    name: null,
    path: null,
    frames: 0,
  });
  const [frameNum, setFrameNum] = useState(0);
  const [points, setPoints] = useState(null);

  useEffect(() => {
    loadDataset();
  }, []);

  const loadDataset = () => {
    if (!validDataset) {
      fetch("/api/loadDataset", {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Failed to load dataset");
          }
        })
        .then((data) => {
          setDatasetInfo({
            path: data.dataset_path,
            name: data.dataset_name,
            frames: data.dataset_len,
          });

          if (data.dataset_len === 0) {
            console.error("Failed to load dataset, please check your dataset");
            console.error(data.dataset_path);
          } else {
            setValidDataset(true);

            console.log(`dataset name: ${datasetInfo.name}`);
            console.log(`dataset path: ${datasetInfo.path}`);
            console.log(`dataset total # frames: ${datasetInfo.frames}`);
          }
        })
        .catch((error) => {
          console.error("Failed to load dataset, please check your backend");
          console.error(error);
        });
    } else {
      console.log("Already loaded dataset...");
    }
  };

  const loadPointCloud = () => {
    const frameNum = frameNum;

    return fetch("/api/loadPointCloud", {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=UTF-8",
      },
      body: JSON.stringify(frameNum),
    })
      .then((response) => {
        if (response.ok) {
          return response.text();
        } else {
          throw new Error("Failed to load point cloud");
        }
      })
      .then((response) => {
        const points = atob(response)
          .split(",")
          .map((x) => parseFloat(x));
        setPoints(points);
      })
      .catch((error) => {
        console.error("Failed to parsing point cloud :-(");
        console.error(error);
        setPoints(null);
      });
  };
}

export default Viewer;
