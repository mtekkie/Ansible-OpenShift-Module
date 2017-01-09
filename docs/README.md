# Ansible Open Shift Container Platform modules
### *Creates and manages Open Shift Projects*

---
### Requirements
* None

---
### Modules

  * [oscp_project - open shift project](#oscp_project)
  * [oscp_buildconfig - open shift buildconfig](#oscp_buildconfig)
  * [oscp_imagestream - open shift service account](#oscp_imagestream)
  * [oscp_deployconfig - open shift deployment config](#oscp_deployconfig)
  * [oscp_serviceaccount - open shift service account](#oscp_serviceaccount)

---

## oscp_project
Open Shift Project

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Project in Open Shift Enterprise.
 The module is using the REST Interface to interact with the Open Shift Master.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| project  |   yes  |  | |  Open Shift Project name  {u'Alias': u'name.'}  |
| state  |   yes  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  If it should be present or absent.  |
| auth_token  |   yes  |  | |  Security Token token for a service account.  |
| master_url  |   yes  |  | |  URL to Open Shift Master server  |



#### Examples

```
- oscp_project:
    master_url: https://funnybunny.middleware.se:8443
    auth_token: eyJhbGciOiJSUzI1NiIsInR5.....
    project: masterminder

```


#### Notes

- In order for this module to work a service account needs to be created.

- It is up to you to decide which project it should have access to.

- {u'In the following example it is given the maximum permissions (cluster admin)': None}

- oc project default

- oc create serviceaccount ansible

- oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:default:ansible

- {u'To get the JWT token to authenticate to the API': None}

- oc describe serviceaccount ansible

- Find the relevant token.

- oc describe secret ansible-token-xxxx


---


## oscp_buildconfig
Open Shift BuildConfig

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Build Config in Open Shift Enterprise.
 The module is using the REST Interface to interact with the Open Shift Master.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   yes  |  | |  Name of build config.  |
| triggers  |   no  |  | |  Triggers determine how new Builds can be launched from a BuildConfig.  If no triggers are defined, a new build can only occur as a result  of an explicit client build creation (v1.BuildTriggerPolicy).  |
| auth_token  |   yes  |  | |  Security Token token for a service account.  |
| serviceAccount  |   no  |  | |  serviceAccount is the name of the ServiceAccount to use to run  the pod created by this build. The pod will be allowed to use  secrets referenced by the ServiceAccount  |
| master_url  |   yes  |  | |  URL to Open Shift Master server  |
| strategy  |   no  |  | |  Build strategy  |
| project  |   yes  |  | |  Open Shift Project  |
| source  |   no  |  | |  source describes the SCM in use.  (v1.BuildSource)  |
| state  |   yes  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  If it should be present or absent.  |
| postCommit  |   no  |  | |  postCommit is a build hook executed after the build output image  is committed, before it is pushed to a registry.  {u'List of v1.BuildPostCommitSpec attributes': None}  command, args, script.  |
| output  |   no  |  | |  output describes the Docker image the Strategy should produce.  {u'List of v1.BuildOutput attributes': None}  to (v1.ObjectReference), pushSecret (v1.LocalObjectReference),  imageLabels(array of v1.ImageLabel)  |
| runPolicy  |   no  |  Serial  | |  RunPolicy describes how the new build created from this build  configuration will be scheduled for execution.  This is optional, if not specified we default to "Serial".  |
| resources  |   no  |  | |  resources computes resource requirements to execute the build.  {u'List of v1.ResourceRequirements attributes': None}  limits, requests  |



#### Examples

```
- oscp_buildconfig:
    master_url: https://funnybunny.middleware.se:8443
    auth_token: eyJhbGciOiJSUzI1NiIsInR5.....
    name: abba
    project: downloader
    triggers: []
    source:
      type: Dockerfile
      dockerfile: 'FROM centos:7
 ENV LANG en_US.UTF-8
 RUN yum install -y epel-release....'
      secrets: null
    strategy:
      type: Docker
      dockerStrategy:
        env:
          - name: MY_BUILD_VAR
            value: Sierra Mike Echo
    output:
      to:
        kind: ImageStreamTag
        namespace: downloader
        name: 'abba:latest'

```


#### Notes

- In order for this module to work a service account needs to be created.

- It is up to you to decide which project it should have access to.

- {u'In the following example it is given the maximum permissions (cluster admin)': None}

- oc project default

- oc create serviceaccount ansible

- oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:default:ansible

- {u'To get the JWT token to authenticate to the API': None}

- oc describe serviceaccount ansible

- Find the relevant token.

- oc describe secret ansible-token-xxxx


---


## oscp_imagestream
Open Shift Service Account

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Handles imagestreams in Open Shift Enterprise.
 The module is using the REST Interface to interact with the Open Shift Master.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| project  |   yes  |  | |  Open Shift Project name  |
| state  |   yes  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  If it should be present or absent.  |
| auth_token  |   yes  |  | |  Security Token token for a service account.  |
| master_url  |   yes  |  | |  URL to Open Shift Master server  |
| name  |   yes  |  | |  Name of imagestream  |



#### Examples

```
- oscp_imagestream:
    master_url: https://funnybunny.middleware.se:8443
    auth_token: eyJhbGciOiJSUzI1NiIsInR5.....
    project: masterminder
    name: dalalven

```


#### Notes

- In order for this module to work a service account needs to be created.

- It is up to you to decide which project it should have access to.

- {u'In the following example it is given the maximum permissions (cluster admin)': None}

- oc project default

- oc create serviceaccount ansible

- oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:default:ansible

- {u'To get the JWT token to authenticate to the API': None}

- oc describe serviceaccount ansible

- Find the relevant token.

- oc describe secret ansible-token-xxxx


---


## oscp_deployconfig
Open Shift Deployment Config

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Build Config in Open Shift Enterprise.
 The module is using the REST Interface to interact with the Open Shift Master.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   yes  |  | |  Name of build config.  |
| triggers  |   no  |  Serial  | |  Triggers determine how updates to a DeploymentConfig result in  new deployments. If no triggers are defined, a new deployment can  only occur as a result of an explicit client update to the  DeploymentConfig with a new LatestVersion  {u'List of Schema': u'v1.DeploymentTriggerPolicy'}  |
| auth_token  |   yes  |  | |  Security Token token for a service account.  |
| replicas  |   no  |  1  | |  Replicas is the number of desired replicas.  Integer  |
| master_url  |   yes  |  | |  URL to Open Shift Master server  |
| strategy  |   yes  |  | |  Strategy describes how a deployment is executed.  {u'Schema': u'v1.DeploymentStrategy'}  |
| project  |   yes  |  | |  Open Shift Project  |
| state  |   yes  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  If it should be present or absent.  |
| template  |   no  |  | |  Template is the object that describes the pod that will be  created if insufficient replicas are detected.  {u'Schema': u'v1.PodTemplateSpec'}  |
| test  |   no  |  False  | |  Test ensures that this deployment config will have zero replicas  except while a deployment is running. This allows the deployment  config to be used as a continuous deployment test - triggering on  images, running the deployment, and then succeeding or failing.  Post strategy hooks and After actions can be used to integrate  successful deployment with an action.  Boolean.  |
| selector  |   no  |  | |  Selector is a label query over pods that should  match the Replicas count.  |



#### Examples

```
- oscp_deployconfig:
    master_url: https://funnybunny.middleware.se:8443
    auth_token: eyJhbGciOiJSUzI1NiIsInR5.....
    strategy:
      type: Rolling
      rollingParams:
        updatePeriodSeconds: 1
        intervalSeconds: 1
        timeoutSeconds: 600
        maxUnavailable: 25%
        maxSurge: 25%
      resources: {  }
    triggers:
      - type: ConfigChange
      - type: ImageChange
        imageChangeParams:
          automatic: true
          containerNames:
            - deluge
          from:
            kind: ImageStreamTag
            name: 'deluge:latest'
    test: false
    selector:
      name: deluge
    template:
      metadata:
        labels:
          name: deluge
      spec:
        volumes:
          - name: virt
            hostPath:
              path: /media/sdc1
          - name: data
            hostPath:
              path: /media/sdc1/deluge
        containers:
          - name: deluge
            ports:
              - containerPort: 8112
                protocol: TCP
              - containerPort: 53160
                protocol: TCP
              - containerPort: 53160
                protocol: UDP
              - containerPort: 58846
                protocol: TCP
            resources: {  }
            volumeMounts:
              - name: virt
                mountPath: /virt
              - name: data
                mountPath: /data
            terminationMessagePath: /dev/termination-log
            imagePullPolicy: Always
        restartPolicy: Always
        terminationGracePeriodSeconds: 30
        dnsPolicy: ClusterFirst
        securityContext: {  }

```


#### Notes

- In order for this module to work a service account needs to be created.

- It is up to you to decide which project it should have access to.

- {u'In the following example it is given the maximum permissions (cluster admin)': None}

- oc project default

- oc create serviceaccount ansible

- oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:default:ansible

- {u'To get the JWT token to authenticate to the API': None}

- oc describe serviceaccount ansible

- Find the relevant token.

- oc describe secret ansible-token-xxxx


---


## oscp_serviceaccount
Open Shift Service Account

  * Synopsis
  * Options
  * Examples

#### Synopsis
 Handles service accounts in Open Shift Enterprise.
 The module is using the REST Interface to interact with the Open Shift Master.

#### Options

| Parameter     | required    | default  | choices    | comments |
| ------------- |-------------| ---------|----------- |--------- |
| name  |   yes  |  | |  Name of Servcie Account  |
| roles  |   no  |  | |  List of roles for servcie account  |
| auth_token  |   yes  |  | |  Security Token token for a service account.  |
| master_url  |   yes  |  | |  URL to Open Shift Master server  |
| project  |   yes  |  | |  Open Shift Project name  |
| state  |   yes  |  present  | <ul> <li>present</li>  <li>absent</li> </ul> |  If it should be present or absent.  |



#### Examples

```
- oscp_serviceaccount:
    master_url: https://funnybunny.middleware.se:8443
    auth_token: eyJhbGciOiJSUzI1NiIsInR5.....
    project: masterminder
    name: servicethis
    roles:
      - system:image-builders
      - system:deployment-controller
      - system:job-controller

```


#### Notes

- In order for this module to work a service account needs to be created.

- It is up to you to decide which project it should have access to.

- {u'In the following example it is given the maximum permissions (cluster admin)': None}

- oc project default

- oc create serviceaccount ansible

- oadm policy add-cluster-role-to-user cluster-admin system:serviceaccount:default:ansible

- {u'To get the JWT token to authenticate to the API': None}

- oc describe serviceaccount ansible

- Find the relevant token.

- oc describe secret ansible-token-xxxx


---


---
Documentation generated by: Created by Network to Code, LLC
For:
2015
