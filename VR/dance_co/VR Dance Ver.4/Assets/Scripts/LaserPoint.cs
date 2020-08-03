using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Valve.VR;
using System.IO;

public class LaserPoint : MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Behaviour_Pose controllerPose;
    public SteamVR_Action_Boolean teleportAction, grabGripAction, menuAction;

    public GameObject MenuObj, laserPrefab;

    GameObject laser, SelectObject, SelectBluePrint;
    SharedObject share;

    Transform laserTransform;
    Vector3 hitPoint;

    List<Vector3> posList = new List<Vector3>();
    List<Vector3> rotList = new List<Vector3>();
    List<string> moveDataList = new List<string>();

    Vector3[] initPos;
    Quaternion[] initRot;

    string basePath, path;
    bool isSave;
    bool[] playList;

    void Start()
    {
        SelectObject = null;
        laser = Instantiate(laserPrefab);
        laserTransform = laser.transform;

        MenuObj.SetActive(false);

        basePath = "./Assets/Resources/";
        path = "";

        share = GameObject.Find("ShareObject").GetComponent<SharedObject>();

        isSave = true;

        int objCnt = GameObject.Find("ObjectList").transform.childCount;
        playList = new bool[objCnt];

        GameObject parent = GameObject.Find("ObjectList").gameObject;

        initPos = new Vector3[objCnt];
        initRot = new Quaternion[objCnt];
        
        for(var i=0;i<objCnt;i++)
        {
            playList[i] = false;
            initPos[i] = parent.transform.GetChild(i).gameObject.transform.position;
            initRot[i] = parent.transform.GetChild(i).gameObject.transform.rotation;
        }
    }

    void Update()
    {
        RaycastHit hit;

        if (Physics.Raycast(controllerPose.transform.position, transform.forward, out hit, 100))
        {
            hitPoint = hit.point;
            if (hit.transform.tag == "Controller" || hit.transform.tag == "Column")
            {
                laser.SetActive(false);
            }

            else
            {
                ShowLaser(hit);
            }

            if (hit.transform.tag == "object")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    if(SelectObject != null)
                    {
                        InitializeObject();
                    }

                    SelectObject = hit.transform.gameObject;
                    setColliderAndRigidBody(false);
                    SelectObject.SetActive(false);
                    share.SelectObject = SelectObject;

                    SelectBluePrint = getBluePrint(SelectObject);
                    SelectBluePrint.SetActive(true);
                    share.SelectBluePrint = SelectBluePrint;

                    path = basePath + hit.transform.name + ".txt";
                }
            }

            if (hit.transform.tag == "blueprint")
            {
                if (teleportAction.GetStateDown(handType))
                {
                    InitializeObject();
                }
            }

            if (hit.transform.tag == "Save")
            {
                if(teleportAction.GetStateDown(handType))
                {
                    DecodeTransformData();
                    SaveData(path);
                    UnityEditor.AssetDatabase.Refresh();

                    posList.Clear();
                    rotList.Clear();
                    moveDataList.Clear();
                    InitializeObject();
                }
            }

            if(hit.transform.tag == "Reset")
            {
                if(teleportAction.GetStateDown(handType))
                {
                    Stop();

                    GameObject parent = GameObject.Find("ObjectList").gameObject;
                    for (var i = 0; i < parent.transform.childCount; i++)
                    {
                        if (SelectObject == parent.transform.GetChild(i).gameObject)
                        {
                            SelectObject.transform.position = initPos[i];
                            SelectObject.transform.rotation = initRot[i];
                            break;
                        }
                    }

                    posList.Clear();
                    rotList.Clear();
                    moveDataList.Clear();
                    InitializeObject();
                }
            }

            if(hit.transform.tag == "Esc")
            {
                if(teleportAction.GetStateDown(handType))
                {
                    MenuObj.SetActive(false);
                }
            }

            if(hit.transform.tag == "Play")
            {
                if(teleportAction.GetStateDown(handType))
                {
                    setColliderAndRigidBody(true);
                    SelectObject.SetActive(true);
                    SelectBluePrint.SetActive(false);

                    GameObject parent = GameObject.Find("ObjectList");
                    for(var i=0;i<parent.transform.childCount;i++)
                    {
                        if(parent.transform.GetChild(i).gameObject == SelectObject)
                        {
                            playList[i] = true;
                            StartCoroutine(playObject(SelectObject, i));
                            break;
                        }
                    }
                }
            }

            if(hit.transform.tag == "Stop")
            {
                if(teleportAction.GetStateDown(handType))
                {
                    Stop();
                }
            }
        }

        else
        {
            laser.SetActive(false);
        }

        SelectObject = share.SelectObject;
        SelectBluePrint = share.SelectBluePrint;

        setText();

        if(menuAction.GetStateDown(handType))
        {
            if (MenuObj.activeSelf)
            {
                MenuObj.SetActive(false);
            }

            else
            {
                MenuObj.SetActive(true);
            }
        }

        if (SelectObject != null && !SelectObject.activeSelf && SelectBluePrint.activeSelf)
        {
            if (GetComponent<FixedJoint>())
            {
                if (isSave)
                {
                    Invoke("addPos", 0.02f);
                    isSave = false;
                }
            }
        }
    }

    void DecodeTransformData()
    {
        for(int i=0;i<posList.Count;i++)
        {
            string transformData;

            transformData = "(" + posList[i].x + ", " + posList[i].y + ", " + posList[i].z + ", " +
                rotList[i].x + ", " + rotList[i].y + ", " + rotList[i].z + ")";

            moveDataList.Add(transformData);
        }
    }

    void ShowLaser(RaycastHit hit)
    {
        laser.SetActive(true);
        laser.transform.position = Vector3.Lerp(controllerPose.transform.position, hitPoint, 0.5f);
        laserTransform.LookAt(hitPoint);
        laserTransform.localScale = new Vector3(laserTransform.localScale.x, laser.transform.localScale.y, hit.distance);
    }

    void addPos()
    {
        posList.Add(SelectBluePrint.transform.position);
        rotList.Add(SelectBluePrint.transform.rotation.eulerAngles);
        isSave = true;
    }

    void InitializeObject()
    {
        setColliderAndRigidBody(true);
        SelectObject.SetActive(true);
        SelectObject = null;
        share.SelectObject = null;

        Destroy(share.SelectBluePrint);
        SelectBluePrint = null;
        share.SelectBluePrint = null;

        posList.Clear();
        rotList.Clear();
        moveDataList.Clear();

        path = "";
    }

    GameObject getBluePrint(GameObject select)
    {
        GameObject blueprint = Instantiate(select);

        if (blueprint.transform.childCount == 0)
        {
            for (var i = 0; i < blueprint.GetComponent<MeshRenderer>().materials.Length; i++)
            {
                blueprint.GetComponent<MeshRenderer>().materials[i].color = new Color(0, 0, 1, 0.5f);
            }
        }

        else
        {
            for (var i = 0; i < blueprint.transform.childCount; i++)
            {
                GameObject child = blueprint.transform.GetChild(i).gameObject;
                for (var j = 0; j < child.GetComponent<MeshRenderer>().materials.Length; j++)
                {
                    child.GetComponent<MeshRenderer>().materials[j].color = new Color(0, 0, 1, 0.5f);
                }
            }
        }

        blueprint.transform.position = select.transform.position;
        blueprint.transform.rotation = select.transform.rotation;

        blueprint.tag = "blueprint";

        return blueprint;
    }

    void SaveData(string filePath)
    {
        FileStream file = new FileStream(filePath, FileMode.Create, FileAccess.Write);
        StreamWriter writer = new StreamWriter(file, System.Text.Encoding.Unicode);

        for (var i=0;i<moveDataList.Count; i++)
        {
            writer.WriteLine(moveDataList[i]);
        }

        writer.Close();
        file.Close();
    }

    void setColliderAndRigidBody(bool active)
    {
        SelectObject.GetComponent<Rigidbody>().isKinematic = active;

        if (SelectObject.GetComponent<SphereCollider>())
        {
            SelectObject.GetComponent<SphereCollider>().isTrigger = active;
        }

        else if (SelectObject.GetComponent<BoxCollider>())
        {
            SelectObject.GetComponent<BoxCollider>().isTrigger = active;
        }

        else if(SelectObject.GetComponent<MeshCollider>())
        {
            SelectObject.GetComponent<MeshCollider>().isTrigger = active;
        }
    }

    void setText()
    {
        if (SelectObject != null)
        {
            MenuObj.transform.GetChild(0).GetComponent<TextMesh>().text = "SelectObject: " + SelectObject.name;
        }

        else if (SelectObject == null)
        {
            MenuObj.transform.GetChild(0).GetComponent<TextMesh>().text = "SelectObject: none";
        }
    }

    void Stop()
    {
        setColliderAndRigidBody(false);
        SelectObject.SetActive(false);
        SelectBluePrint.SetActive(true);

        GameObject parent = GameObject.Find("ObjectList");
        for (var i = 0; i < parent.transform.childCount; i++)
        {
            if (parent.transform.GetChild(i).gameObject == SelectObject)
            {
                SelectObject.transform.position = initPos[i];
                SelectObject.transform.rotation = initRot[i];
                playList[i] = false;
                break;
            }
        }
    }

    IEnumerator playObject(GameObject obj, int idx)
    {
        List<Vector3> pos = new List<Vector3>();
        List<Vector3> rot = new List<Vector3>();

        for(var i=0;i<posList.Count; i++)
        {
            pos.Add(posList[i]);
            rot.Add(rotList[i]);
        }

        obj.transform.position = pos[0];
        obj.transform.rotation = Quaternion.Euler(rot[0]);

        var j = 0;
        Debug.Log("InCoroutine");
        while(playList[idx])
        {
            Debug.Log("InWhile");
            obj.transform.position = pos[j];
            obj.transform.rotation = Quaternion.Euler(rot[j]);

            j++;

            if(j==pos.Count)
            {
                j = 0;
                obj.transform.position = pos[0];
                obj.transform.rotation = Quaternion.Euler(rot[0]);
            }

            yield return new WaitForSeconds(0.02f);
        }
    }
}
